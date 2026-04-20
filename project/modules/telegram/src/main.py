from datetime import datetime
import os
import sys
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from zoneinfo import ZoneInfo

from _paths import FATE_CORE_SRC_DIR, get_env_file
from branding import attach_branding, get_branding_payload, get_disclaimer_payload
from utils.timezone import now_cn

if str(FATE_CORE_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(FATE_CORE_SRC_DIR))

try:
    load_dotenv(get_env_file(), override=False)
except FileNotFoundError:
    pass

SERVICE_HOST = os.getenv("FATE_SERVICE_HOST", "0.0.0.0")
SERVICE_PORT = int(os.getenv("FATE_SERVICE_PORT", "8001"))

from models import (
    BaziRequest,
    BaziResponse,
    BaziData,
    BrandingInfo,
    TimeInfo,
    Meta,
    LiuyaoFactorRequest,
    LiuyaoFactorResponse,
    LiuyaoFactorData,
)
from bazi_calculator import BaziCalculator
from report_generator import DEFAULT_HIDE as REPORT_HIDE
import db_v2 as db
from liuyao_factors import generate_factor
from fate_core.usecases import PureAnalysisInput, calculate_pure_analysis

app = FastAPI(title="八字排盘服务", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def _branding_model() -> BrandingInfo:
    return BrandingInfo(**get_branding_payload())


def _disclaimer_model() -> str:
    return get_disclaimer_payload()


@app.exception_handler(HTTPException)
async def branded_http_exception_handler(_request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=attach_branding(
            {
                "success": False,
                "error": str(exc.detail),
                "statusCode": exc.status_code,
            }
        ),
    )


@app.exception_handler(RequestValidationError)
async def branded_validation_exception_handler(_request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=attach_branding(
            {
                "success": False,
                "error": "请求参数无效",
                "details": exc.errors(),
                "statusCode": 422,
            }
        ),
    )


@app.exception_handler(Exception)
async def branded_exception_handler(_request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=attach_branding(
            {
                "success": False,
                "error": str(exc),
                "statusCode": 500,
            }
        ),
    )


@app.get("/health")
def health():
    return attach_branding({"status": "ok"})


def _parse_bazi_request(req: BaziRequest) -> tuple[datetime, float, float]:
    birth_dt = datetime.strptime(f"{req.birthDate} {req.birthTime}", "%Y-%m-%d %H:%M:%S")
    if not req.birthPlace:
        raise HTTPException(status_code=400, detail="birthPlace 必填（经纬度用于真太阳时/风水/占星）")
    return birth_dt, req.birthPlace.longitude, req.birthPlace.latitude


@app.post("/api/v1/bazi/simple")
def calculate_bazi_simple(req: BaziRequest):
    """简化八字计算 - 直接返回原始结果"""
    try:
        birth_dt, longitude, latitude = _parse_bazi_request(req)
        
        calculator = BaziCalculator(
            birth_dt,
            req.gender,
            longitude,
            latitude=latitude,
            name=req.name,
            birth_place=req.birthPlace.name,
            use_true_solar_time=req.options.useTrueSolarTime,
        )
        result = calculator.calculate(hide=REPORT_HIDE)
        
        return attach_branding({"success": True, "data": result})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/bazi/pure-analysis")
def calculate_bazi_pure_analysis(req: BaziRequest):
    """纯命理分析 - 仅返回配置约束下的核心字段。"""
    try:
        birth_dt, longitude, latitude = _parse_bazi_request(req)
        payload = PureAnalysisInput(
            birth_dt=birth_dt,
            gender=req.gender,
            longitude=longitude,
            latitude=latitude,
            name=req.name,
            birth_place=req.birthPlace.name,
            use_true_solar_time=req.options.useTrueSolarTime,
        )
        result = calculate_pure_analysis(payload)
        return attach_branding(
            {
                "success": True,
                "data": result,
                "meta": {
                    "calculatedAt": now_cn().isoformat(),
                    "profile": "pure_analysis",
                },
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/bazi/calculate", response_model=BaziResponse)
def calculate_bazi(req: BaziRequest, user_id: Optional[str] = None):
    """计算八字排盘"""
    try:
        birth_dt, longitude, latitude = _parse_bazi_request(req)
        
        calculator = BaziCalculator(
            birth_dt,
            req.gender,
            longitude,
            latitude=latitude,
            name=req.name,
            birth_place=req.birthPlace.name,
            use_true_solar_time=req.options.useTrueSolarTime,
        )
        result = calculator.calculate(hide=REPORT_HIDE)
        
        tz = ZoneInfo(req.birthPlace.timezone)
        ts_dt = calculator.true_solar_time if req.options.useTrueSolarTime else birth_dt
        time_info = TimeInfo(
            inputTime=birth_dt.replace(tzinfo=tz).isoformat(),
            trueSolarTime=ts_dt.replace(tzinfo=tz).isoformat() if req.options.useTrueSolarTime else None,
            lunarDate=f"{result['fourPillars']['year']['fullName']}年",
            solarTerm="",
        )
        
        data = BaziData(
            timeInfo=time_info,
            fourPillars=result["fourPillars"],
            hiddenStems=result.get("hiddenStems", {}),
            tenGods=result.get("tenGods", {}),
            fiveElements=result.get("fiveElements", {}),
            dayMaster=result.get("dayMaster", {}),
            majorFortune=result.get("majorFortune", {}),
            annualFortune=result.get("annualFortune", []),
            voidBranches=result.get("voidInfo", {}),
        )
        
        # 保存到数据库
        record_id = None
        if user_id:
            biz_data = {"input": req.model_dump(), "result": data.model_dump()}
            record_id = db.save_record(user_id, "bazi", biz_data)
        
        return BaziResponse(
            disclaimer=_disclaimer_model(),
            success=True,
            data=data,
            meta=Meta(calculatedAt=now_cn().isoformat(), recordId=record_id),
            branding=_branding_model(),
        )
    except Exception as e:
        return BaziResponse(
            disclaimer=_disclaimer_model(),
            success=False,
            error=str(e),
            meta=Meta(calculatedAt=now_cn().isoformat()),
            branding=_branding_model(),
        )


@app.post("/api/v1/liuyao/factor", response_model=LiuyaoFactorResponse)
def calculate_liuyao_factor(req: LiuyaoFactorRequest):
    """六爻量化因子 - 统一输出结构"""
    try:
        factor = generate_factor(
            item=req.item,
            timestamp=req.timestamp,
            method=req.method,
            seed=req.seed,
            cnts=req.cnts,
            cycle_hint=req.cycleHint,
        )
        data = LiuyaoFactorData(**factor.to_dict())
        return LiuyaoFactorResponse(
            disclaimer=_disclaimer_model(),
            success=True,
            data=data,
            meta=Meta(calculatedAt=now_cn().isoformat(), algorithm="liuyao-divicast", version="1.0.0"),
            branding=_branding_model(),
        )
    except Exception as e:
        return LiuyaoFactorResponse(
            disclaimer=_disclaimer_model(),
            success=False,
            error=str(e),
            meta=Meta(calculatedAt=now_cn().isoformat(), algorithm="liuyao-divicast", version="1.0.0"),
            branding=_branding_model(),
        )


@app.get("/api/v1/records/{record_id}")
def get_record(record_id: int):
    """获取记录"""
    record = db.get_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    return attach_branding({"success": True, "data": record})


@app.get("/api/v1/user/{user_id}/records")
def get_user_records(user_id: str, biz_type: str = None, limit: int = 10):
    """获取用户记录"""
    records = db.get_user_records(user_id, biz_type, limit)
    return attach_branding({"success": True, "data": records, "total": len(records)})


@app.delete("/api/v1/records/{record_id}")
def delete_record(record_id: int):
    """删除记录"""
    if db.delete_record(record_id):
        return attach_branding({"success": True})
    raise HTTPException(status_code=404, detail="Not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=SERVICE_HOST, port=SERVICE_PORT)
