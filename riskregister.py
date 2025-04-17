import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class RiskRegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Protector Network Risk Register")
        self.risks = []

        # Header frame for program name
        header = tk.Label(root, text="Protector Network Risk Register", font=("Arial", 16, "bold"))
        header.pack(pady=10)

        # Organization name input
        org_frame = tk.Frame(root)
        org_frame.pack(pady=5)
        tk.Label(org_frame, text="Organization Name:").grid(row=0, column=0, sticky="e")
        self.org_entry = tk.Entry(org_frame)
        self.org_entry.grid(row=0, column=1)

        # Risk input frame
        input_frame = tk.LabelFrame(root, text="Add a Risk")
        input_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(input_frame, text="Risk Description:").grid(row=0, column=0, sticky="e")
        self.desc_entry = tk.Entry(input_frame, width=40)
        self.desc_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Likelihood (1-5):").grid(row=1, column=0, sticky="e")
        self.likelihood = tk.StringVar(value="3")
        ttk.Combobox(input_frame, textvariable=self.likelihood, values=["1", "2", "3", "4", "5"], width=5).grid(row=1, column=1, sticky="w", padx=5, pady=2)

        tk.Label(input_frame, text="Impact (1-5):").grid(row=2, column=0, sticky="e")
        self.impact = tk.StringVar(value="3")
        ttk.Combobox(input_frame, textvariable=self.impact, values=["1", "2", "3", "4", "5"], width=5).grid(row=2, column=1, sticky="w", padx=5, pady=2)

        add_btn = tk.Button(input_frame, text="Add Risk", command=self.add_risk)
        add_btn.grid(row=3, columnspan=2, pady=5)

        # Treeview to display risks
        tree_frame = tk.Frame(root)
        tree_frame.pack(padx=10, pady=5, fill="both", expand=True)
        columns = ("Description", "Likelihood", "Impact")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        # Generate report button
        gen_btn = tk.Button(root, text="Generate Register & Heatmap", command=self.generate_report)
        gen_btn.pack(pady=10)

    def add_risk(self):
        desc = self.desc_entry.get().strip()
        lik = self.likelihood.get()
        imp = self.impact.get()
        if not desc:
            messagebox.showwarning("Input Error", "Risk description cannot be empty.")
            return
        self.risks.append({"Description": desc, "Likelihood": int(lik), "Impact": int(imp)})
        self.tree.insert("", tk.END, values=(desc, lik, imp))
        self.desc_entry.delete(0, tk.END)

    def generate_report(self):
        org = self.org_entry.get().strip() or "Organization"
        if not self.risks:
            messagebox.showwarning("No Risks", "Please add at least one risk before generating the report.")
            return
        # Create DataFrame
        df = pd.DataFrame(self.risks)
        # Save register
        filename = f"{org}_risk_register.csv"
        df.to_csv(filename, index=False)
        messagebox.showinfo("Report Generated", f"Risk register saved to {filename}")

        # Pivot table for heatmap
        pivot = df.pivot_table(index="Impact", columns="Likelihood", aggfunc="size", fill_value=0)
        plt.figure(figsize=(6,5))
        sns.heatmap(pivot, annot=True, fmt="d", cmap="Reds")
        plt.title(f"{org} Risk Heatmap")
        plt.xlabel("Likelihood")
        plt.ylabel("Impact")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = RiskRegisterApp(root)
    root.mainloop()
