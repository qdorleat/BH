import pandas as pd


def export_to_excel(df, output_path):
    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:

        sheet_name = output_path.stem[:31]  # limite Excel

        df.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False
        )

        workbook = writer.book
        worksheet = writer.sheets[sheet_name]

        date_format = workbook.add_format({
            "num_format": "dd.mm.yyyy"
        })

        for idx, col in enumerate(df.columns):
            max_len = max(
                df[col].astype(str).map(len).max(),
                len(col)
            )

            # Works only with datetime format
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                worksheet.set_column(
                    idx,
                    idx,
                    max(max_len + 2, 12),
                    date_format
                )
            else:
                worksheet.set_column(
                    idx,
                    idx,
                    max_len + 2
                )
