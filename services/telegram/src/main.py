"""八字排盘微服务 API"""
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional
from utils.timezone import now_cn
from _paths import BAZI_DB_DIR

sys.path.insert(0, str(BAZI_DB_DIR))

from models import (
    BaziRequest,
    BaziResponse,
    BaziData,
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

app = FastAPI(title="八字排盘服务", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/bazi/simple")
def calculate_bazi_simple(req: BaziRequest):
    """简化八字计算 - 直接返回原始结果"""
    try:
        birth_dt = datetime.strptime(f"{req.birthDate} {req.birthTime}", "%Y-%m-%d %H:%M:%S")
        if not req.birthPlace:
            raise HTTPException(status_code=400, detail="birthPlace 必填（经纬度用于真太阳时/风水/占星）")
        longitude = req.birthPlace.longitude
        latitude = req.birthPlace.latitude
        
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
        
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/bazi/calculate", response_model=BaziResponse)
def calculate_bazi(req: BaziRequest, user_id: Optional[str] = None):
    """计算八字排盘"""
    try:
        birth_dt = datetime.strptime(f"{req.birthDate} {req.birthTime}", "%Y-%m-%d %H:%M:%S")
        if not req.birthPlace:
            raise HTTPException(status_code=400, detail="birthPlace 必填（经纬度用于真太阳时/风水/占星）")
        longitude = req.birthPlace.longitude
        latitude = req.birthPlace.latitude
        
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
            success=True,
            data=data,
            meta=Meta(calculatedAt=now_cn().isoformat(), recordId=record_id),
        )
    except Exception as e:
        return BaziResponse(success=False, error=str(e), meta=Meta(calculatedAt=now_cn().isoformat()))


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
            success=True,
            data=data,
            meta=Meta(calculatedAt=now_cn().isoformat(), algorithm="liuyao-divicast", version="1.0.0"),
        )
    except Exception as e:
        return LiuyaoFactorResponse(
            success=False,
            error=str(e),
            meta=Meta(calculatedAt=now_cn().isoformat(), algorithm="liuyao-divicast", version="1.0.0"),
        )


@app.get("/api/v1/records/{record_id}")
def get_record(record_id: int):
    """获取记录"""
    record = db.get_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    return {"success": True, "data": record}


@app.get("/api/v1/user/{user_id}/records")
def get_user_records(user_id: str, biz_type: str = None, limit: int = 10):
    """获取用户记录"""
    records = db.get_user_records(user_id, biz_type, limit)
    return {"success": True, "data": records, "total": len(records)}


@app.delete("/api/v1/records/{record_id}")
def delete_record(record_id: int):
    """删除记录"""
    if db.delete_record(record_id):
        return {"success": True}
    raise HTTPException(status_code=404, detail="Not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
