# Scripts Directory

## 📁 目录结构

### 📊 reports/
报告生成脚本
- `generate_complete_output.py` - 完整输出测试脚本
- `generate_full_report.py` - 全量66字段完整报告生成器
- `generate_user_report.py` - 用户友好的排版报告生成器
- `扩展功能具体内容.py` - 扩展功能具体内容展示

### 🔧 setup/
环境配置脚本
- `setup_external_env.sh` - 外部环境依赖自动配置脚本
- `bootstrap_fatecat.sh` - 一键安装依赖并启动 FateCat 服务

## 🚀 使用方法

### 生成报告
```bash
cd scripts/reports
python3 generate_user_report.py
```

### 配置环境
```bash
cd scripts/setup
chmod +x setup_external_env.sh
./setup_external_env.sh

chmod +x bootstrap_fatecat.sh
./bootstrap_fatecat.sh deps
```
