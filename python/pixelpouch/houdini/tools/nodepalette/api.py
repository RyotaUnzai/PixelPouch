from typing import Callable, Optional

CreateNodeFunc = Callable[[str], None]

create_node: Optional[CreateNodeFunc] = None
