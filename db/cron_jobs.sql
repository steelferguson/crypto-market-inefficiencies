[?1049h[22;0;0t[?1h= jobid |  schedule  |             command             
-------+------------+---------------------------------
     1 | 10 0 1 * * | CALL drop_old_partition()
     2 | 15 0 1 * * | CALL create_monthly_partition()
(2 rows)

[7m(END)[27m[K[K[?1l>[?1049l[23;0;0t