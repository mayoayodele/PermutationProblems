# PermutationProblems
CQM solution methods for permutation problems





## Constraint Handling Methods


```math
a_1(x) = \left ( 1- \sum_{i=1}^n x_{i,j} \right )^2
```

```math
a_2(x) = \left ( 1- \sum_{i=1}^n x_{j,i} \right )^2
```

```math
g_1(x) = \sum_{j=1}^n a_1(x)
```

```math
g_2(x) = \sum_{j=1}^n a_2(x)
```



|                       | Vertical one-hot | Horizontal one-hot |Implementation of Constraints                                                                    |
| --------------------- | -----------------| ------------------ |-------------------------------------------------------------------------------------------------|
| tsp_cqm1/ qap_cqm1    | $g_1$            | $g_2$              |add_constraint( $g_1$ ), add_constraint( $g_2$ )                                                 |
| tsp_cqm2/ qap_cqm2    | $g_1$            | $g_2$              |add_constraint($g_1 + g_2$)                                                                      |
| tsp_cqm2/ qap_cqm2    | $g_1$            | add_discrete       |add_constraint($g_1$)                                                                            |
| tsp_cqm4/ qap_cqm4    | $a_1$            | $a_2$              |add_constraint($a_1i$), add_constraint($a_2i$) $\forall$ $i$ $\in$ {1,...,n}  |
| tsp_cqm5/ qap_cqm5    | $a_1$            |add_discrete        |add_constraint($a_1i$) $\forall$ $i$ $\in$ {1,...,n}  |
