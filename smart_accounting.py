
Enter "help" below or click "Help" above for more information.
>>> import tkinter as tk
... from tkinter import ttk, messagebox, filedialog
... import pandas as pd
... import matplotlib.pyplot as plt
... from datetime import datetime
... 
... class SmartAccountingSystem:
...     def __init__(self, root):
...         self.root = root
...         self.root.title("النظام المحاسبي الذكي")
...         self.root.geometry("1200x700")
...         
...         # بيانات أولية
...         self.data = {
...             "المبيعات": pd.DataFrame(columns=["التاريخ", "العميل", "المبلغ", "العملة"]),
...             "المصروفات": pd.DataFrame(columns=["التاريخ", "المورد", "المبلغ", "العملة"]),
...             "المخزون": pd.DataFrame(columns=["الصنف", "الكمية", "سعر الوحدة", "حد إعادة الطلب"])
...         }
...         
...         # تبويبات
...         self.tab_control = ttk.Notebook(root)
...         
...         self.entry_tab = ttk.Frame(self.tab_control)
...         self.report_tab = ttk.Frame(self.tab_control)
...         self.audit_tab = ttk.Frame(self.tab_control)
...         self.settings_tab = ttk.Frame(self.tab_control)
...         
...         self.tab_control.add(self.entry_tab, text="إدخال البيانات")
...         self.tab_control.add(self.report_tab, text="التقارير")
...         self.tab_control.add(self.audit_tab, text="الرقابة")
...         self.tab_control.add(self.settings_tab, text="الإعدادات")
...         
...         self.tab_control.pack(expand=1, fill="both")
...         
        # واجهة إدخال البيانات
        self.create_entry_tab()
        
        # واجهة التقارير
        self.create_report_tab()
        
        # واجهة الرقابة
        self.create_audit_tab()
        
        # واجهة الإعدادات
        self.create_settings_tab()

    def create_entry_tab(self):
        """واجهة إدخال البيانات"""
        ttk.Label(self.entry_tab, text="اختر نوع العملية:").grid(row=0, column=0, padx=5, pady=5)
        self.operation_type = ttk.Combobox(self.entry_tab, values=["المبيعات", "المصروفات", "المخزون"])
        self.operation_type.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.entry_tab, text="البيانات:").grid(row=1, column=0, padx=5, pady=5)
        self.data_entry = tk.Text(self.entry_tab, height=5, width=50)
        self.data_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(self.entry_tab, text="إضافة", command=self.add_entry).grid(row=2, column=1, pady=10)
    
    def create_report_tab(self):
        """واجهة التقارير"""
        ttk.Label(self.report_tab, text="اختر نوع التقرير:").pack(pady=5)
        self.report_type = ttk.Combobox(self.report_tab, values=["المبيعات", "المصروفات", "المخزون"])
        self.report_type.pack(pady=5)
        
        ttk.Button(self.report_tab, text="عرض التقرير", command=self.generate_report).pack(pady=5)
        
        self.report_tree = ttk.Treeview(self.report_tab)
        self.report_tree.pack(expand=1, fill="both")
    
    def create_audit_tab(self):
        """واجهة الرقابة"""
        ttk.Button(self.audit_tab, text="تشغيل الفحص الرقابي", command=self.audit_data).pack(pady=10)
        self.audit_output = tk.Text(self.audit_tab, height=20, width=100)
        self.audit_output.pack(pady=10)
    
    def create_settings_tab(self):
        """واجهة الإعدادات"""
        ttk.Button(self.settings_tab, text="تحديث أسعار العملات", command=self.update_external_data).pack(pady=10)
        ttk.Button(self.settings_tab, text="تصدير إلى Excel", command=self.export_to_excel).pack(pady=10)

    def add_entry(self):
        """إضافة قيد جديد"""
        entry_type = self.operation_type.get()
        raw_data = self.data_entry.get("1.0", tk.END).strip()
        
        if not entry_type or not raw_data:
            messagebox.showerror("خطأ", "الرجاء إدخال جميع البيانات")
            return
        
        try:
            if entry_type == "المبيعات":
                date, client, amount, currency = raw_data.split(",")
                new_row = {"التاريخ": date.strip(), "العميل": client.strip(), "المبلغ": float(amount), "العملة": currency.strip()}
            elif entry_type == "المصروفات":
                date, supplier, amount, currency = raw_data.split(",")
                new_row = {"التاريخ": date.strip(), "المورد": supplier.strip(), "المبلغ": float(amount), "العملة": currency.strip()}
            else:  # المخزون
                item, qty, price, reorder = raw_data.split(",")
                new_row = {"الصنف": item.strip(), "الكمية": int(qty), "سعر الوحدة": float(price), "حد إعادة الطلب": int(reorder)}
            
            self.data[entry_type] = pd.concat([self.data[entry_type], pd.DataFrame([new_row])], ignore_index=True)
            messagebox.showinfo("تم", "تمت إضافة البيانات بنجاح")
            self.data_entry.delete("1.0", tk.END)
        
        except Exception as e:
            messagebox.showerror("خطأ", f"صيغة البيانات غير صحيحة\n{e}")

    def generate_report(self):
        """إنشاء تقرير"""
        report_type = self.report_type.get()
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        
        if not self.data[report_type].empty:
            self.report_tree["columns"] = list(self.data[report_type].columns)
            self.report_tree["show"] = "headings"
            for col in self.data[report_type].columns:
                self.report_tree.heading(col, text=col)
            for _, row in self.data[report_type].iterrows():
                values = tuple(row.get(col, "") for col in self.report_tree["columns"])
                self.report_tree.insert("", tk.END, values=values)

    def audit_data(self):
        """التدقيق المحاسبي"""
        self.audit_output.delete("1.0", tk.END)
        issues = []
        
        for dtype, df in self.data.items():
            if dtype in ["المبيعات", "المصروفات"] and not df.empty:
                for i, row in df.iterrows():
                    if row["المبلغ"] <= 0:
                        issues.append(f"⚠ {dtype}: قيمة غير منطقية في الصف {i+1} - المبلغ = {row['المبلغ']}")
            if dtype == "المخزون" and not df.empty:
                for i, row in df.iterrows():
                    if row["الكمية"] <= row["حد إعادة الطلب"]:
                        issues.append(f"⚠ المخزون: الصنف {row['الصنف']} وصل حد إعادة الطلب")
        
        if issues:
            self.audit_output.insert(tk.END, "\n".join(issues))
        else:
            self.audit_output.insert(tk.END, "✅ لا توجد أخطاء محاسبية")

    def update_external_data(self):
        """تحديث أسعار العملات (محاكاة)"""
        messagebox.showinfo("تحديث", "تم تحديث أسعار العملات من المصدر الخارجي (محاكاة)")

    def export_to_excel(self):
        """تصدير البيانات إلى ملف Excel"""
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if not file_path:
            return
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            for dtype, df in self.data.items():
                df.to_excel(writer, sheet_name=dtype, index=False)
        messagebox.showinfo("تم", f"تم تصدير البيانات إلى {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartAccountingSystem(root)
    root.mainloop()

