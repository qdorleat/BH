import pandas as pd

def export_to_excel(df, output_path):
    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        df.to_excel(
            writer,
            sheet_name=output_path.name,
            index=False
        )

        worksheet = writer.sheets[output_path.name]

        for idx, col in enumerate(df.columns):
            max_len = max(
                df[col].astype(str).map(len).max(),
                len(col)
            )
            worksheet.set_column(idx, idx, max_len + 2)
