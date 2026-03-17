# utils/file_importer.py
import os
import re
import threading
import pandas as pd
from tkinter import filedialog

class FileImporter:
    """文件导入工具类"""
    
    def __init__(self, app):
        self.app = app
    
    def import_single(self, tag, btn_widget, scope, data_vault, m1_storage, callback=None):
        """
        单个导入表格
        
        参数:
            tag: 标签名称
            btn_widget: 按钮组件（用于更新状态）
            scope: 作用域
            data_vault: 数据存储字典
            m1_storage: 文件路径存储字典
            callback: 导入完成后的回调函数
        """
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        d_scope = self._get_display_name(scope)
        
        file_path = filedialog.askopenfilename(
            title=f"选择 [{tag}] 的表格文件",
            initialdir=downloads_path,
            filetypes=[("表格文件", "*.xlsx *.xls *.csv")]
        )
        
        if not file_path:
            self.app.add_log("取消", "文件导入", f"<{d_scope}> 取消{tag} 选择")
            return
        
        def process_data():
            try:
                self.app.after(0, lambda: btn_widget.config(text="⏳ 读取中...", fg="#FFA500"))
                
                if file_path.lower().endswith('.csv'):
                    try:
                        df = pd.read_csv(file_path, encoding='utf-8')
                    except:
                        df = pd.read_csv(file_path, encoding='gbk')
                else:
                    df = pd.read_excel(file_path)
                
                data_vault[tag] = df
                m1_storage[tag] = file_path
                
                file_name = os.path.basename(file_path)
                
                def update_ui():
                    btn_widget.config(text=f"✅ 已选择({len(df)})", fg="#00FF00")
                    self.app.add_log("成功", "文件导入", f"<{d_scope}> 导入 {tag}: ({file_name})")
                    if callback:
                        callback(tag, df)
                
                self.app.after(0, update_ui)
                
            except Exception as e:
                self.app.after(0, lambda: self.app.add_log("失败", "文件导入", f"<{d_scope}> 导入 {tag} 失败: {str(e)}"))
                self.app.after(0, lambda: btn_widget.config(text="❌ 读取失败", fg="#FF4444"))
        
        threading.Thread(target=process_data, daemon=True).start()
    
    def batch_import(self, target_list, import_labels, import_status_labels, 
                     abcd_status_label=None, bh3_status_label=None, batch_name=None):
        """
        批量导入表格 - 统一接口
        
        参数:
            target_list: 目标标签列表
            import_labels: 左侧标签字典
            import_status_labels: 左侧状态标签字典
            abcd_status_label: ABCD状态标签
            bh3_status_label: BH3状态标签
            batch_name: 批量名称 ("ABCD" 或 "BH3")
        
        返回:
            success_count: 成功数量
            failed_list: 失败列表
        """
        success_list = []
        failed_list = []
        
        # 选择文件夹
        folder_path = filedialog.askdirectory(
            title=f"选择 [{batch_name}] 批量导入目录",
            initialdir=os.path.join(os.path.expanduser("~"), "Desktop")
        )
        
        if not folder_path:
            self.app.add_log("取消", "批量导入", f"{batch_name}操作已取消")
            return 0, []
        
        # 获取文件夹中的所有文件
        all_files = os.listdir(folder_path)
        
        for tag in target_list:
            found = False
            matched_file = None
            
            for file_name in all_files:
                if not file_name.lower().endswith(('.xlsx', '.xls', '.csv')):
                    continue
                
                # 获取不带扩展名的文件名
                pure_name = os.path.splitext(file_name)[0]
                
                # 精确匹配：文件名必须完全等于标签
                if pure_name == tag:
                    matched_file = file_name
                    found = True
                    break
            
            if found and matched_file:
                file_path = os.path.join(folder_path, matched_file)
                try:
                    # 读取文件
                    if matched_file.lower().endswith('.csv'):
                        try:
                            df = pd.read_csv(file_path, encoding='utf-8')
                        except:
                            df = pd.read_csv(file_path, encoding='gbk')
                    else:
                        df = pd.read_excel(file_path)
                    
                    # 存储数据
                    self.app.data_vault[tag] = df
                    self.app.M1_data_storage[tag] = file_path
                    
                    # 更新左侧标签状态
                    if tag in import_labels:
                        import_labels[tag].config(fg="#00FF7F")  # C_SUCCESS
                    if tag in import_status_labels:
                        import_status_labels[tag].config(
                            text=f"已选择({len(df)}行)", fg="#00FF7F"
                        )
                    
                    success_list.append(tag)
                    
                except Exception as e:
                    self.app.add_log("失败", "批量导入", f"【{tag}】导入失败: {str(e)}")
                    failed_list.append(tag)
            else:
                self.app.add_log("警告", "批量导入", f"未找到匹配文件: {tag}")
                failed_list.append(tag)
        
        # 更新批量状态标签
        total = len(target_list)
        success = len(success_list)
        
        if batch_name == "ABCD" and abcd_status_label:
            abcd_status_label.config(text=f"{success}/{total}")
            abcd_status_label.config(fg="#00FF7F" if success == total else "#D4AF37")
        elif batch_name == "BH3" and bh3_status_label:
            bh3_status_label.config(text=f"{success}/{total}")
            bh3_status_label.config(fg="#00FF7F" if success == total else "#D4AF37")
        
        # 日志提示
        if failed_list:
            failed_names = "、".join(failed_list)
            self.app.add_log("警告", "批量导入", f"{batch_name}表格导入失败: {failed_names}")
        else:
            self.app.add_log("成功", "批量导入", f"{batch_name}表格全部导入成功 ({success}/{total})")
        
        return success, failed_list
    
    def _get_display_name(self, scope):
        """获取显示名称"""
        name_map = {
            "ALPHA": getattr(self.app, "alpha", "表格筛选"),
            "BETA": getattr(self.app, "beta", "表格区分"),
            "SOUSUO": getattr(self.app, "sousuo", "综合搜索"),
        }
        return name_map.get(scope, scope)
