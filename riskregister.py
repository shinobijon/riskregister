import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import textwrap

class RiskRegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Protector Network Risk Register")
        self.risks = []
        self.editing_item = None

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

        self.add_btn = tk.Button(input_frame, text="Add Risk", command=self.add_or_update_risk)
        self.add_btn.grid(row=3, columnspan=2, pady=5)

        # Treeview to display risks
        tree_frame = tk.Frame(root)
        tree_frame.pack(padx=10, pady=5, fill="both", expand=True)
        columns = ("Description", "Likelihood", "Impact")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        # Edit/Delete buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Edit Selected Risk", command=self.edit_risk).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Delete Selected Risk", command=self.delete_risk).grid(row=0, column=1, padx=5)

        # Generate report button
        gen_btn = tk.Button(root, text="Generate Register & Heatmap", command=self.generate_report)
        gen_btn.pack(pady=10)

    def add_or_update_risk(self):
        desc = self.desc_entry.get().strip()
        lik = self.likelihood.get()
        imp = self.impact.get()
        if not desc:
            messagebox.showwarning("Input Error", "Risk description cannot be empty.")
            return

        if self.editing_item:
            idx = self.tree.index(self.editing_item)
            self.risks[idx] = {"Description": desc, "Likelihood": int(lik), "Impact": int(imp)}
            self.tree.item(self.editing_item, values=(desc, lik, imp))
            self.editing_item = None
            self.add_btn.config(text="Add Risk")
        else:
            self.risks.append({"Description": desc, "Likelihood": int(lik), "Impact": int(imp)})
            self.tree.insert("", tk.END, values=(desc, lik, imp))

        self.desc_entry.delete(0, tk.END)

    def edit_risk(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a risk to edit.")
            return
        item = selected[0]
        idx = self.tree.index(item)
        risk = self.risks[idx]
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, risk["Description"])
        self.likelihood.set(str(risk["Likelihood"]))
        self.impact.set(str(risk["Impact"]))
        self.editing_item = item
        self.add_btn.config(text="Save Changes")

    def delete_risk(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a risk to delete.")
            return
        item = selected[0]
        idx = self.tree.index(item)
        del self.risks[idx]
        self.tree.delete(item)

    def generate_report(self):
        org = self.org_entry.get().strip() or "Organization"
        if not self.risks:
            messagebox.showwarning("No Risks", "Please add at least one risk before generating the report.")
            return

        df = pd.DataFrame(self.risks)
        filename = f"{org}_risk_register.csv"
        df.to_csv(filename, index=False)
        messagebox.showinfo("Report Generated", f"Risk register saved to {filename}")

        # Prepare counts and wrapped descriptions
        count_pivot = df.pivot_table(index="Impact", columns="Likelihood", aggfunc="size", fill_value=0)
        desc_pivot = df.groupby(["Impact", "Likelihood"])['Description'] \
                       .apply(lambda x: '\n'.join(x)) \
                       .unstack(fill_value="")
        # Wrap text to width of ~20 chars
        desc_wrapped = desc_pivot.applymap(lambda val: '\n'.join(textwrap.wrap(val, width=20)))

        plt.figure(figsize=(8,6))
        ax = sns.heatmap(
            count_pivot,
            annot=desc_wrapped,
            fmt="",
            cmap="Reds",
            cbar=False,
            annot_kws={"fontsize": 8}
        )
        plt.title(f"{org} Risk Heatmap")
        plt.xlabel("Likelihood")
        plt.ylabel("Impact")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = RiskRegisterApp(root)
    root.mainloop()
