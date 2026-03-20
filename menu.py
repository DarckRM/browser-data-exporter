import sys
import subprocess

def main_menu():
    while True:
        print("\n===== 主菜单 =====")
        print("1. 协同")
        print("2. 财务")
        print("3. 退出")
        choice = input("请输入选项 (1/2/3): ").strip()

        if choice == "1":
            submenu_xietong()
        elif choice == "2":
            submenu_caiwu()
        elif choice == "3":
            print("👋 已退出程序")
            break
        else:
            print("❌ 输入无效，请重新选择")


def submenu_xietong():
    while True:
        print("\n--- 协同子菜单 ---")
        print("1. 销售合同")
        print("2. 采购合同")
        print("3. 返回主菜单")
        choice = input("请输入选项 (1/2/3): ").strip()

        if choice == "1":
            print("👉 正在进入【销售合同】模块 (XTXSHT.py)...")
            subprocess.run([sys.executable, "XTXSHT.py"])
        elif choice == "2":
            print("👉 正在进入【采购合同】模块 (XTCGHT.py)...")
            subprocess.run([sys.executable, "XTCGHT.py"])
        elif choice == "3":
            print("↩️ 返回主菜单")
            break
        else:
            print("❌ 输入无效，请重新选择")


def submenu_caiwu():
    while True:
        print("\n--- 财务子菜单 ---")
        print("1. 发票管理")
        print("2. 报销申请")
        print("3. 返回主菜单")
        choice = input("请输入选项 (1/2/3): ").strip()

        if choice == "1":
            print("👉 执行【发票管理】功能")
            # 这里也可以调用其他 py 文件
        elif choice == "2":
            print("👉 执行【报销申请】功能")
            # 这里也可以调用其他 py 文件
        elif choice == "3":
            print("↩️ 返回主菜单")
            break
        else:
            print("❌ 输入无效，请重新选择")


if __name__ == "__main__":
    main_menu()