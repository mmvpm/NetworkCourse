```
[Node "0"] init dv: {'0': 0, '1': 1, '2': 3, '3': 7}
[Node "1"] init dv: {'0': 1, '1': 0, '2': 1}
[Node "2"] init dv: {'0': 3, '1': 1, '2': 0, '3': 2}       
[Node "3"] init dv: {'0': 7, '2': 2, '3': 0}
[Node "0"] dv has changed: {'0': 0, '1': 1, '2': 2}        
[Node "1"] dv has changed: {'0': 4, '1': 0, '2': 1, '3': 3}
[Node "2"] dv has changed: {'0': 9, '2': 0, '3': 2}        
[Node "3"] dv has changed: {'0': 7, '1': 8, '2': 9, '3': 0}
[Node "0"] dv has changed: {'0': 0, '1': 1, '2': 2, '3': 5}
[Node "1"] dv has changed: {'0': 1, '1': 0, '2': 1, '3': 3}
[Node "2"] dv has changed: {'0': 3, '1': 4, '2': 0, '3': 2}
[Node "3"] dv has changed: {'0': 7, '1': 8, '2': 2, '3': 0}
[Node "0"] dv has changed: {'0': 0, '1': 1, '2': 2, '3': 4}
[Node "2"] dv has changed: {'0': 3, '1': 1, '2': 0, '3': 2}
[Node "3"] dv has changed: {'0': 5, '1': 6, '2': 2, '3': 0}
[Node "2"] dv has changed: {'0': 2, '1': 1, '2': 0, '3': 2}
[Node "3"] dv has changed: {'0': 5, '1': 3, '2': 2, '3': 0}
[Node "3"] dv has changed: {'0': 4, '1': 3, '2': 2, '3': 0}
[Node "0"] scheduled notify_neighbors()
[Node "2"] scheduled notify_neighbors()
[Node "1"] scheduled notify_neighbors()
[Node "3"] scheduled notify_neighbors()
[Main] set 1 -> 2 weight to 6
[Node "2"] weights has changed: {'0': 3, '1': 6, '3': 2}
[Main] set 0 -> 2 weight to 7
[Node "2"] dv has changed: {'0': 2, '1': 6, '2': 0, '3': 2}
[Node "1"] weights has changed: {'0': 1, '2': 6}
[Node "2"] dv has changed: {'0': 3, '1': 4, '2': 0, '3': 2}
[Node "0"] weights has changed: {'1': 1, '2': 7, '3': 7}
[Main] set 0 -> 3 weight to 2
[Node "0"] dv has changed: {'0': 0, '1': 1, '2': 7, '3': 4}
[Node "1"] dv has changed: {'0': 1, '1': 0, '2': 6, '3': 3}
[Node "3"] dv has changed: {'0': 5, '1': 6, '2': 2, '3': 0}
[Node "2"] weights has changed: {'0': 7, '1': 6, '3': 2}
[Node "0"] dv has changed: {'0': 0, '1': 1, '2': 2, '3': 4}
[Node "3"] weights has changed: {'0': 2, '2': 2}
[Node "1"] dv has changed: {'0': 1, '1': 0, '2': 6, '3': 8}
[Node "3"] dv has changed: {'0': 2, '1': 6, '2': 2, '3': 0}
[Node "0"] weights has changed: {'1': 1, '2': 7, '3': 2}
[Node "3"] dv has changed: {'0': 2, '1': 3, '2': 2, '3': 0}
[Node "0"] dv has changed: {'0': 0, '1': 1, '2': 2, '3': 2}
[Node "2"] dv has changed: {'0': 7, '1': 4, '2': 0, '3': 2}
[Node "0"] dv has changed: {'0': 0, '1': 1, '2': 4, '3': 2}
[Node "2"] dv has changed: {'0': 7, '1': 6, '2': 0, '3': 2}
[Node "1"] dv has changed: {'0': 1, '1': 0, '2': 5, '3': 3}
[Node "2"] dv has changed: {'0': 4, '1': 5, '2': 0, '3': 2}
[Node "0"] scheduled notify_neighbors()
[Node "2"] scheduled notify_neighbors()
<...>
[Node "3"] scheduled notify_neighbors()
[Node "0"] final dv: {'0': 0, '1': 1, '2': 4, '3': 2}
[Node "2"] final dv: {'0': 4, '1': 5, '2': 0, '3': 2}
[Node "1"] final dv: {'0': 1, '1': 0, '2': 5, '3': 3}
[Node "3"] final dv: {'0': 2, '1': 3, '2': 2, '3': 0}
```