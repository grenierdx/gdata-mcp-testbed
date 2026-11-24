from typing import Any, Optional

from pydantic import BaseModel, Field, model_validator


class ColumnDetail(BaseModel):
    field: str = Field(description="Column name")
    type: str = Field(description="Column data type")
    collation: Optional[str] = Field("The collation used for this column's values; only relevant for non-binary string columns")
    null: bool = Field(description="Whether the column is nullable")
    key: str = Field(description="Which key the column belongs to, if any; PRI for the primary key")
    default: Optional[str] = Field(description="The default value for this column")
    extra: str = Field("Extra details about this column, such as auto_increment")
    privileges: str = Field("The privileges you have for this column, such as select")
    comment: str = Field("A description of what this column's values mean")

    @model_validator(mode="before")
    @classmethod
    def lowercase_keys_apply_bool(cls, data: Any):
        if not isinstance(data, dict):
            return data
        normalized = {}
        for key, value in data.items():
            key = key.lower() if isinstance(key, str) else key
            if key in normalized:
                raise ValueError(f"duplicate key after case normalization: {key}")
            normalized[key] = value
        print(normalized)
        normalized['null'] = True if normalized['null'] == 'YES' else False
        return normalized
