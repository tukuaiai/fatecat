"""
请求限流与队列机制
- 全局并发限制
- 用户级别限流
- 请求队列
"""
import asyncio
import time
from collections import defaultdict
from functools import wraps

# ========== 配置 ==========
MAX_CONCURRENT = 1          # 最大同时计算数
USER_COOLDOWN = 600         # 用户冷却时间（秒）= 10分钟
USER_DAILY_LIMIT = 3        # 每用户每日限制
QUEUE_MAX_SIZE = 9999       # 队列无限制

# ========== 状态 ==========
_semaphore = asyncio.Semaphore(MAX_CONCURRENT)
_user_last_request = defaultdict(float)  # user_id -> timestamp
_user_daily_count = defaultdict(int)     # user_id -> count
_daily_reset_time = 0                    # 上次重置时间
_queue_size = 0


def _reset_daily_if_needed():
    """每日重置计数"""
    global _daily_reset_time, _user_daily_count
    now = time.time()
    # 每24小时重置
    if now - _daily_reset_time > 86400:
        _user_daily_count.clear()
        _daily_reset_time = now


def check_rate_limit(user_id: int) -> tuple[bool, str]:
    """
    检查用户是否可以发起请求
    返回: (是否允许, 拒绝原因)
    """
    global _queue_size
    _reset_daily_if_needed()
    
    now = time.time()
    
    # 检查冷却
    last = _user_last_request.get(user_id, 0)
    if now - last < USER_COOLDOWN:
        wait = int(USER_COOLDOWN - (now - last))
        return False, f"请等待 {wait} 秒后再试"
    
    # 检查每日限制
    if _user_daily_count[user_id] >= USER_DAILY_LIMIT:
        return False, f"今日已达上限 ({USER_DAILY_LIMIT} 次)，明天再来"
    
    # 检查队列
    if _queue_size >= QUEUE_MAX_SIZE:
        return False, "服务器繁忙，请稍后再试"
    
    return True, ""


def record_request(user_id: int):
    """记录用户请求"""
    _user_last_request[user_id] = time.time()
    _user_daily_count[user_id] += 1


async def acquire_slot():
    """获取计算槽位"""
    global _queue_size
    _queue_size += 1
    await _semaphore.acquire()


def release_slot():
    """释放计算槽位"""
    global _queue_size
    _queue_size = max(0, _queue_size - 1)
    _semaphore.release()


def get_queue_status() -> dict:
    """获取队列状态"""
    return {
        "concurrent": MAX_CONCURRENT - _semaphore._value,
        "max_concurrent": MAX_CONCURRENT,
        "queue_size": _queue_size,
        "queue_max": QUEUE_MAX_SIZE,
    }


def rate_limit(func):
    """装饰器：自动限流"""
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        
        allowed, reason = check_rate_limit(user_id)
        if not allowed:
            await update.message.reply_text(f"⏳ {reason}")
            return
        
        record_request(user_id)
        
        try:
            await acquire_slot()
            return await func(update, context, *args, **kwargs)
        finally:
            release_slot()
    
    return wrapper
