## bp

simple binary packer/unpacker.

### Usage

```python
from bp import *

user = Struct(
    Field("Name", String(length=4), "Alex"),
    Field("Age", Int8, 24),
    Field("Weight", Int8, 98),
)

user.set("Age", 25)

with write_stream("user.dat") as out_stream:
    user.write(out_stream)

with read_stream("user.dat") as in_stream:
    user.read(in_stream)
    print(user.get("Age"))  # 24
```
