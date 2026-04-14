#!/usr/bin/env python3
"""
姓名学功能演示脚本
基于 bazi-name-master 库的五格剖象法
"""

from src.xingming import calc_wuge, suggest_names, analyze_name_elements
import json

def demo_wuge_analysis():
    """演示五格分析功能"""
    print("=" * 50)
    print("五格剖象法姓名分析演示")
    print("=" * 50)
    
    test_names = [
        ("王", "小明"),
        ("李", "华强"),
        ("张", "三丰"),
        ("刘", "德华"),
        ("陈", "美丽")
    ]
    
    for xing, ming in test_names:
        print(f"\n【分析姓名】: {xing}{ming}")
        try:
            result = calc_wuge(xing, ming)
            print(f"总分: {result['score']} 分 ({result['level']})")
            print(f"五行搭配: {' + '.join(result['xingElements'] + result['mingElements'])}")
            
            print("五格详情:")
            for ge_name, ge_data in result['wuge'].items():
                print(f"  {ge_name}: {ge_data['shu']}数 - {ge_data['jixiong']}")
                
        except Exception as e:
            print(f"分析失败: {e}")
        
        print("-" * 30)


def demo_name_suggestions():
    """演示姓名推荐功能"""
    print("\n" + "=" * 50)
    print("智能姓名推荐演示")
    print("=" * 50)
    
    test_cases = [
        ("李", ["木", "火"], 80),
        ("王", ["土", "金"], 75),
        ("张", ["火", "木"], 85),
        ("陈", ["火", "土"], 70)
    ]
    
    for xing, elements, target_score in test_cases:
        print(f"\n【推荐条件】: 姓氏={xing}, 五行={'+'.join(elements)}, 目标分数>={target_score}")
        
        try:
            suggestions = suggest_names(xing, target_score=target_score, target_elements=elements)
            
            if suggestions:
                print(f"推荐了 {len(suggestions)} 个高分名字:")
                for i, name_data in enumerate(suggestions[:5], 1):
                    chars_info = " + ".join(name_data['chars'])
                    print(f"  {i}. {name_data['name']} - {name_data['score']}分")
                    print(f"     字符: {chars_info}")
            else:
                print("未找到符合条件的名字，建议降低分数要求")
                
        except Exception as e:
            print(f"推荐失败: {e}")
        
        print("-" * 40)


def demo_element_analysis():
    """演示五行分析功能"""
    print("\n" + "=" * 50)
    print("姓名五行分析演示")
    print("=" * 50)
    
    test_names = ["张三丰", "李小龙", "王菲", "刘德华", "陈奕迅"]
    
    for name in test_names:
        print(f"\n【分析姓名】: {name}")
        
        try:
            result = analyze_name_elements(name)
            print(f"主导五行: {result['dominantElement']}")
            
            print("字符详情:")
            for char_data in result['chars']:
                print(f"  {char_data['char']}: {char_data['strokes']}画, "
                      f"{char_data['element']}行, 读音: {char_data['sound']}")
            
            print("五行统计:")
            for element, count in result['elementCount'].items():
                if count > 0:
                    print(f"  {element}: {count}个")
                    
        except Exception as e:
            print(f"分析失败: {e}")
        
        print("-" * 30)


def main():
    """主函数"""
    print("🔮 基于 bazi-name-master 库的姓名学分析系统")
    print("📚 采用传统五格剖象法，包含6000+汉字数据库")
    
    # 演示所有功能
    demo_wuge_analysis()
    demo_name_suggestions() 
    demo_element_analysis()
    
    print("\n" + "=" * 50)
    print("✅ 姓名学功能演示完成")
    print("💡 可通过 Telegram Bot 或 API 调用这些功能")
    print("=" * 50)


if __name__ == "__main__":
    main()
