# The Optimization Vocabulary

One thousand two hundred seventy-two named concepts that engineering uses to
talk about making programs cheaper, folded from a catalog of 9,188 named,
established entries; the research record beside this file preserves how. The
entries sit in six families, ordered as a decision passes through them: what
analysis can tell you, how a cheaper computation is chosen, what the toolchain
already does, how work is fitted to the machine, how work reaches someone, and
how any of it is measured and decided. Read the family you are standing in,
and treat each entry as an option to weigh, so an omission becomes a decision
rather than an accident.

Most entries name something a person applies, and those end by naming their
price, because a technique with no stated price reads as free and none of them
is. Entries that name a measurement, a model, a law, or a class of problem end
at the definition, since knowing them costs nothing. That split is the first
finding, and it falls in a sharper place than the word "optimization" suggests:
the vocabulary of analysis never makes anything faster, the vocabulary of the
toolchain describes work already being done for whoever compiles, and the
decisions that belong to a person are concentrated in the middle families.

One boundary is deliberate. Mathematical optimization, the discipline of
minimizing objective functions, shares the word with this study and is a
different field. Gradient descent, linear and convex programming, and the
metaheuristics are not catalogued here.

## What analysis can tell you

### Asymptotic notation

- **Big-O notation**, also **big-oh**: upper bound on growth up to a constant factor; f is O(g) when f grows no faster than g.
- **Big-Theta notation**: simultaneous upper and lower bound; f is Theta(g) when the two functions grow at the same rate.
- **Big-Omega notation**: lower bound on growth up to a constant factor; f is Omega(g) when f grows at least as fast as g.
- **Little-o notation**, also **little-omega notation**: strict bounds, holding when the ratio of f to g tends to zero or to infinity respectively.
- **Tight bound**: a bound matched from above and below, so no asymptotically better bound of the same form exists.
- **Soft-O notation**, also **O-tilde**: big-O with polylogarithmic factors suppressed, the notation standing behind the phrase near-linear time.
- **Hidden constant**, also **constant factor**: the coefficient asymptotic notation discards, large enough in some algorithms to void the bound's practical value.

### Orders of growth

- **Polynomial time**: cost bounded by a fixed power of input size, with named rungs constant, logarithmic, linear, linearithmic, quadratic, and cubic.
- **Sublinear time**: cost growing more slowly than input size, so the algorithm cannot read all of its input.
- **Exponential time**: cost bounded by a constant raised to a polynomial in input size, with factorial and doubly exponential growth above it.
- **Subexponential time**: cost growing more slowly than any fixed exponential in input size.
- **Pseudo-polynomial time**: cost polynomial in the numeric value of the input rather than in its bit length.
- **Iterated logarithm and inverse Ackermann growth**: the near-constant growth rates log-star of n and inverse Ackermann, met in union-find and Davenport-Schinzel bounds.
- **Galactic algorithm**: an algorithm whose superior asymptotic bound never takes effect, its crossover point lying beyond every input size of practical interest.

### Cases and input distributions

- **Worst case**: the greatest cost over all inputs of a given size, a guarantee resting on no distributional assumption; the best case is the least such cost.
- **Average case**, also **expected running time**: the mean cost over a stated distribution on inputs, or over the algorithm's own coin flips.
- **Distributional assumption**: the input distribution an average-case bound depends on, uniform inputs or uniformly random arrival order, without which the bound says nothing.
- **Pathological input**: an input constructed to elicit an algorithm's worst case, such as a sorted array for naive quicksort.

### Amortized analysis

- **Amortized analysis**: bounding a whole operation sequence's cost and dividing, so costly operations are paid for by cheap ones, at the price of guaranteeing nothing about individual latency.
- **Aggregate method**, also **aggregate analysis**: bound the sequence's total cost directly and divide by operation count, at the price of assigning every operation type the same figure.
- **Accounting method**, also **banker's method**: charge each operation a fixed price and bank the surplus as credit for later costly operations, at the price of a price schedule guessed in advance.
- **Potential method**, also **physicist's method**: define a potential on structure state so amortized cost is actual cost plus potential change, at the price of requiring the potential be invented.
- **Debit method**: amortization for lazy structures, assigning debits to suspensions that must be discharged before forcing, at the price of persistence-aware bookkeeping.
- **Deamortization**: convert an amortized bound into a worst-case per-operation bound by spreading rebuilding work, at the price of bookkeeping and a constant-factor slowdown.
- **Global rebuilding**: deamortize by maintaining a shadow copy advanced incrementally by each operation, at the price of roughly doubled space.
- **Partial rebuilding**: rebuild an unbalanced subtree wholesale when a weight condition breaks, at the price of occasional expensive operations.

### Beyond worst-case analysis

- **Smoothed analysis**: expected cost on worst-case inputs after small random perturbation, interpolating between worst-case and average-case measures.
- **Competitive analysis**: measuring an online algorithm's cost against the optimal offline cost on the same request sequence, their worst-case ratio being the competitive ratio.
- **Online adversary models**: the oblivious, adaptive online, and adaptive offline opponents, differing in when they commit to requests and what they must themselves pay.
- **Random-order model**: the adversary chooses the input set while the arrival order is a uniformly random permutation.
- **Resource augmentation**: comparing an algorithm holding extra speed or capacity against an optimum holding less, used where competitive ratios are unbounded.
- **Output-sensitive analysis**: expressing cost bounds in output size alongside input size, so cheap answers cost little.
- **Adaptive analysis**: cost bounds that shrink as the input approaches an already solved form, stated against a presortedness measure such as inversion count.
- **Instance optimality**: matching, within a constant factor, the best cost achievable by any algorithm on every individual instance.

### Recurrences and sums

- **Divide-and-conquer recurrence**: the form T(n) equals a times T(n over b) plus f(n), which most analyses of recursive algorithms reduce to.
- **Master theorem**: solve that recurrence by comparing f(n) against n to the log base b of a, at the price of excluding unbalanced or irregular splits.
- **Akra-Bazzi method**: solve it with unequal subproblem sizes and floor perturbations admitted, at the price of evaluating an integral.
- **Recursion tree**, also **iteration method**: unroll the recurrence level by level until a summable pattern emerges, at the price of producing a guess rather than a proof.
- **Substitution method**: guess a bound and confirm it by induction, at the price of requiring the answer be guessed before it can be proved.
- **Characteristic equation method**, also **annihilator method**: solve a constant-coefficient linear recurrence from the roots of its characteristic polynomial, at the price of applying only to that form.
- **Telescoping**, also **summation by parts**: sum consecutive differences so interior terms cancel, at the price of first rewriting the recurrence as a difference.
- **Stirling's approximation and the harmonic number**: the two standing identities of cost analysis, the growth of n factorial and the log n plus Euler constant sum of reciprocals.
- **Generating function analysis**: encode a cost sequence as a power series and read asymptotics from its dominant singularity, at the price of analytic machinery and obscured combinatorial meaning.

### Probabilistic analysis

- **Chernoff bound**, also **Hoeffding's inequality**: exponentially decaying tail bound for sums of independent bounded variables, the workhorse behind bounds holding with high probability.
- **Markov's and Chebyshev's inequalities**: the weak tail bounds from the mean alone and from the variance, decaying linearly and quadratically in the deviation.
- **Union bound**: a bound on the probability that any of several bad events occurs, obtained by summing their probabilities.
- **Bounded differences inequality**, also **McDiarmid's inequality**: concentration for functions that change little when any single coordinate changes.
- **Azuma's inequality**: exponential tail bound for martingales with bounded differences, applied by exposing the input one part at a time as a Doob martingale.
- **Balls-into-bins model**: items thrown independently into bins uniformly at random, the model behind coupon collector arguments and the birthday collision threshold.
- **Probabilistic method**: prove an object exists by showing a random object has the property with positive probability, at the price of yielding no construction.
- **Backward analysis**: analyse a randomized incremental construction by treating the last inserted element as uniformly random, at the price of applying only to order-independent constructions.
- **Derandomization**: replace true randomness by conditional expectations or a pseudorandom generator, at the price of larger running time or an unproven hardness assumption.

### Cost analysis carried out on programs

- **Empirical scaling analysis**: fit measured running times to a growth model to estimate practical order, at the price of extrapolating past the sizes measured.
- **Doubling experiment**: time an implementation at successively doubled input sizes and read the growth exponent from successive ratios, at the price of assuming a pure power law.
- **Static cost analysis**: derive cost bounds mechanically from program text by extracting a recurrence, at the price of conservatism wherever control flow depends on data.
- **Worst-case execution time analysis**: compute a safe upper bound on a real-time program's execution time, at the price of pessimism from hardware state that cannot be modeled.
- **Automatic amortized resource analysis**: infer amortized bounds by a type system assigning potential to data structures, at the price of restriction to the bound templates the system supports.
- **Termination analysis**: prove a program halts by exhibiting a ranking function that strictly decreases, at the price of failing on loops governed by unmodeled state.
- **Halting problem**: the undecidable question whether a program terminates, which with Rice's theorem is the root limit on all mechanical cost analysis.

### Machines and cost models

- **Cost model**: the stated set of chargeable operations and their prices in which a bound is proved, the choice that decides what looks fast.
- **RAM model**, also **random access machine**: charges one time unit per arithmetic operation and per indexed memory access, whatever the magnitude of the operands.
- **Logarithmic cost criterion**: the RAM convention charging in proportion to operand bit length, closing the unit-cost model's loophole on arbitrarily large integers.
- **Word RAM**: a RAM whose cells hold w bits with constant-time arithmetic on whole words; the transdichotomous convention lets bounds exploit w being at least log n.
- **Real RAM**: exact unit-cost arithmetic and comparison on real numbers, the standard setting of computational geometry.
- **Cell-probe model**: charges only for memory cell accesses and gives computation away free, the setting for data structure lower bounds.
- **Comparison model**: charges only for comparisons between elements, the setting of the n log n sorting bound.
- **Turing machine model**: a tape-based model whose step count defines time complexity; multitape variants differ from the single-tape model by at most a square.
- **Boolean circuit model**: measures the size and depth of a gate network on fixed-length input, a non-uniform model since every input length gets its own circuit.

### Memory hierarchy and locality

- **External memory model**, also **disk access machine**: counts transfers of B-record blocks between a memory of M records and unbounded disk, charging nothing for computation.
- **I/O complexity**, also **cache complexity**: the number of block transfers, equivalently cache misses, a computation incurs at a stated memory and block size.
- **Cache-oblivious model**: demands one algorithm be optimal at every unknown block and cache size, at the price of forfeiting the tuning cache-aware code enjoys.
- **External memory bounds**: the four floors, N over B transfers to scan, that figure times log base M-over-B of it to sort or permute, log base B of N to search.
- **Communication-avoiding lower bound**: a bound on the words a computation must move, derived from its dependency structure rather than its operation count.
- **Locality of reference**: the clustering of accesses in time and in address space, temporal and spatial respectively, the premise every hierarchy model exploits.
- **Stack distance**, also **reuse distance**: the distinct addresses touched between two references to one address, predicting hit or miss and summarized by a miss ratio curve.
- **Three Cs model**: the classification of cache misses as compulsory, capacity, or conflict.

### Query, streaming, and communication measures

- **Query complexity**: the number of input accesses an algorithm requires, counted in place of running time, the deterministic case being decision tree depth.
- **Streaming model**: few sequential passes over the input while holding memory sublinear in its size, pass count and sketch size being the reported costs.
- **Turnstile model**: a streaming model whose updates both increase and decrease item counts; the cash register model permits increases only.
- **Sliding window model**: a streaming model in which only the most recent items count toward the answer.
- **Adversarially robust streaming**: a streaming guarantee that survives an adversary who observes the algorithm's own answers.
- **Property testing**: distinguishing objects that have a property from those far from having it, in a number of queries independent of input size.
- **Certificate complexity**: the number of input positions that must be fixed to force a function's value.
- **Sensitivity and block sensitivity**: the largest number of single-coordinate flips, or of disjoint blocks, whose flipping changes a function's value, polynomially tied to every decision tree measure.
- **Communication complexity**: the bits two parties must exchange to compute a function whose input is split between them, counted alongside rounds.

### Parallel and distributed cost models

- **Work-span model**, also **work-depth model**: summarizes a parallel computation by total work and longest dependency chain, whose ratio is the parallelism usefully employable.
- **Brent's theorem**: a greedy scheduler finishes within work over p plus span on p processors.
- **PRAM**: a shared-memory model with synchronized processors and unit-cost shared access, graded EREW, CREW, and CRCW by which concurrent accesses are permitted.
- **BSP model**: supersteps pairing local computation with communication and closing on a barrier, priced by gap and latency parameters.
- **LogP model**: prices latency, per-message overhead, bandwidth gap, and processor count with no global barrier; LogGP adds a per-byte gap for long messages.
- **LOCAL and CONGEST models**: synchronous distributed rounds with unbounded messages in LOCAL and logarithmic-size messages in CONGEST, so CONGEST charges bandwidth as well as rounds.
- **Massively Parallel Computation model**: machines with sublinear memory exchanging data in synchronous rounds, charging rounds and total communication.

### Space, resources, and hardware ceilings

- **Space complexity**: the memory a computation requires as a function of input size, called auxiliary space when the input storage is excluded and in-place when that is constant.
- **Time-space tradeoff**: the relation whereby one resource falls only as the other grows, sharpened by proven lower bounds on their product.
- **Succinct space**: space exceeding the information-theoretic minimum by only a lower-order additive term; compact space stays within a constant factor of it.
- **Preprocessing, query, and update time**: the three costs a data structure reports alongside its space, query time falling only as stored space grows.
- **Roofline model**: bounds attainable rate by peak compute on one side and bandwidth times arithmetic intensity on the other, meeting at the machine balance ridge point.
- **Compute-bound, memory-bound, and latency-bound**: the three regimes, named by whether arithmetic throughput, memory bandwidth, or the latency of dependent operations caps performance.
- **CPU performance equation**, also **iron law of performance**: runtime equals instruction count times cycles per instruction times cycle time.

### Complexity classes

- **P**: problems decidable in polynomial time on a deterministic machine.
- **NP**: problems whose yes-answers admit polynomial-time verifiable certificates; co-NP does the same for no-answers, and factoring style problems sit in both.
- **PSPACE**: problems decidable in polynomial space with running time unbounded, equal to nondeterministic polynomial space by Savitch's theorem.
- **EXPTIME**: problems decidable in time exponential in a polynomial of input size, with EXPSPACE and doubly exponential time above it.
- **L and NL**: problems decidable in logarithmic work space deterministically and nondeterministically, NL closed under complement by the Immerman-Szelepcsenyi theorem.
- **BPP**: polynomial time with bounded two-sided error; RP and co-RP err on one side only, and ZPP never errs while running in expected polynomial time.
- **Sharp-P**, also **#P**: functions counting the accepting paths of a nondeterministic polynomial-time machine, hard even for problems whose decision version lies in P.
- **Polynomial hierarchy**: the ladder above NP graded by quantifier alternations into levels Sigma-k and Pi-k, where equality of two adjacent levels collapses everything above.
- **Circuit classes**: the non-uniform ladder from AC0 of constant depth, through counting-gate ACC0 and threshold-gate TC0, to NC1 and polylogarithmic-depth NC.
- **BQP**: problems decidable with bounded error by a polynomial-size quantum circuit, QMA being its certificate analogue.

### Hardness, completeness, and conjectures

- **NP-completeness**: lying in NP and being as hard as every NP problem, established for satisfiability by the Cook-Levin theorem; NP-hardness drops the membership requirement.
- **Polynomial-time reduction**: map one problem's instances into another's in polynomial time, at the price of blurring every distinction finer than a polynomial factor.
- **Strongly NP-hard**: hard even when all numeric inputs are polynomially bounded, so no pseudo-polynomial algorithm exists; weakly NP-hard problems leave room for one.
- **Completeness beyond NP**: PSPACE-complete typified by quantified Boolean formula truth, NL-complete by directed reachability, P-complete under log-space reduction by circuit evaluation, EXPTIME-complete by generalized board games.
- **Fixed-parameter tractability**: solvability in f of the parameter times a polynomial in input size; XP admits n to the f, and W-hierarchy hardness evidences neither.
- **Approximation ratio**: the worst-case ratio between an algorithm's answer and the optimum, naming the class APX, the schemes PTAS and FPTAS, and the thresholds proved through the PCP theorem.
- **Fine-grained hardness conjectures**: the Exponential Time Hypothesis and its strong form, with the 3SUM, orthogonal vectors, all-pairs shortest paths, and online matrix-vector conjectures, sources of conditional polynomial lower bounds.

### Lower bounds and barriers

- **Lower bound**: a proof that no algorithm within a stated model achieves less than a given cost, unconditional when proved outright and conditional when derived from a hardness conjecture.
- **Information-theoretic lower bound**: a floor from the number of outcomes an algorithm must distinguish, yielding the log of n factorial comparisons any comparison sort performs.
- **Adversary argument**: prove a floor by an opponent answering queries so as to keep the answer undetermined as long as possible, at the price of applying only in query-style models.
- **Counting argument**: prove a floor from the pigeonhole gap between the number of objects and the number of short descriptions, at the price of naming no specific hard instance.
- **Reduction-based lower bound**: transfer a floor from a problem already known hard, at the price of depending entirely on the source problem's standing.
- **Yao's minimax principle**: the best randomized algorithm's worst-case cost equals the best deterministic cost against the hardest input distribution.
- **Communication lower bound methods**: the fooling set, the rank of the communication matrix, discrepancy over large rectangles, corruption, and the lifting theorems that carry query bounds across.
- **Dynamic data structure lower bound methods**: the chronogram method, partitioning an update sequence into epochs by age, and information transfer, bounding what must cross a time interval.
- **Time and space hierarchy theorems**: more time, or more space, strictly decides more languages, proved by diagonalization against an enumeration of machines.
- **Barriers to lower bound proofs**: relativization defeats oracle-invariant arguments, natural proofs defeats large constructive circuit arguments, algebrization covers algebraic extensions of both.

## Choosing a cheaper computation

### Reshaping the problem

- **Divide and conquer**: split an instance into independent subinstances of the same kind and combine their solutions, at the price of recursion overhead and combine work.
- **Decrease and conquer**, also the **incremental approach**: reduce the instance by a constant or a factor and extend the smaller solution, at the price of recursion depth linear in that reduction.
- **Transform and conquer**, also **instance simplification**: preprocess the input into a form a cheaper solver accepts, such as sorting it first, at the price of the preprocessing pass and a mapping back.
- **Representation change**: re-encode the data in a structure whose operations are cheaper, at the price of conversion time and a second representation held in memory.
- **Problem reduction**: map the problem onto a different problem with a known fast solver, at the price of transformation work and total dependence on that solver.
- **Prune and search**: discard a constant fraction of the input at each step before recursing, at the price of the work spent proving that fraction irrelevant.
- **Coordinate compression**, also **discretization**: replace values by their rank so arrays can be indexed by them, at the price of a sort, a mapping table, and lost resolution between values.
- **Layered graph construction**: encode extra state as copies of the graph so a plain search suffices, at the price of a graph multiplied by the state count.
- **Fork-join decomposition**: spawn subtasks recursively and join their results, at the price of task creation overhead at fine granularity.
- **Parallel prefix scan**: compute all prefixes in logarithmic depth by combining partial results, at the price of roughly doubling the total work.
- **Wavefront parallelism**, also **diagonal decomposition**: compute along antidiagonals so dependencies are honoured, at the price of parallel width that varies through the run.

### Dynamic programming formulation

- **Dynamic programming**: solve each overlapping subproblem once and reuse the stored result, at the price of memory proportional to the state space.
- **Optimal substructure and overlapping subproblems**: the two properties an instance must carry before dynamic programming applies, optimal parts composing an optimal whole and a recursion that reaches the same subproblem many times.
- **Memoization**, also **top-down dynamic programming**, also **tabling**: cache each recursive call's result keyed by its arguments, at the price of recursion overhead and table or hash space.
- **Tabulation**, also **bottom-up dynamic programming**: fill the table in dependency order without recursion, at the price of computing states the answer never needs.
- **Rolling array**: keep only the table layers a transition still reads, at the price of losing the information needed to reconstruct the solution.
- **Hirschberg's technique**: recover an alignment in linear space by splitting at a midpoint found from two half-scores, at the price of doubling the running time.
- **Bitmask dynamic programming**, also **state compression**: index states by a subset stored as the bits of an integer, at the price of a table exponential in the set size.
- **Sum over subsets transform**, also the **zeta transform**: aggregate over all subsets of every mask in n times two to the n steps, inverted by the Mobius transform, at the price of a full mask-indexed table.
- **Fast Walsh-Hadamard transform**: compute exclusive-or convolutions in n times two to the n steps, at the price of holding transformed copies of both arrays.
- **Interval dynamic programming**: index states by a contiguous segment and split it at an inner point, at the price of cubic time in the segment count.
- **Dynamic programming on trees**: compute each node's value from its children in one post-order pass, at the price of a table stored per node.
- **Rerooting technique**: derive every node's whole-tree answer from one upward pass and one downward pass, at the price of requiring an invertible merge.

### Named dynamic programming speedups

- **Knuth's optimization**, also the **Knuth-Yao speedup**: restrict each split point search to the range between neighbouring optimal splits, at the price of proving the quadrangle inequality on the cost array.
- **Divide and conquer optimization**, also **monotone minima**: recurse on halves of the index range once optimal splits are known to be monotone, at the price of proving that monotonicity.
- **Convex hull trick**: keep candidate linear transitions on a hull and query the best one, at the price of requiring sorted slopes or a balanced structure.
- **Li Chao tree**: store candidate lines in a segment tree over the query domain so insertion order is free, at the price of a logarithmic factor per query.
- **Monotone queue optimization**, also **deque optimization**: hold window candidates in a monotone deque so each transition is amortized constant, at the price of requiring monotone windows.
- **Slope trick**: represent a convex piecewise linear value function by its breakpoints in a heap, at the price of requiring convexity at every step.
- **Prefix sum optimization of transitions**: replace a range of transitions by a precomputed running total, at the price of requiring an invertible aggregate.
- **Matrix exponentiation of a recurrence**: raise the transition matrix to a power by repeated squaring to skip steps, at the price of a cubic factor in the state count.
- **Bitset optimization**: replace an inner boolean loop of the recurrence with word-parallel bitset operations, at the price of losing per-item reconstruction detail.
- **Four Russians technique**: precompute results for small blocks of the table and look them up, at the price of a table exponential in block size.
- **Binary splitting of multiplicities**: rewrite a bounded count as power-of-two bundles so a bounded knapsack becomes a binary one, at the price of logarithmically many extra items.

### Greedy choice and local improvement

- **Greedy method**: commit to the locally best choice at each step and never revise it, at the price of correctness unless the problem carries the matching structure.
- **Exchange argument**, also the **greedy stays ahead argument**: prove a greedy order optimal by swapping a rival solution stepwise into it, at the price of a case analysis over every swap.
- **Matroid structure**: independence system with the exchange property, on which taking elements in weight order is optimal, relaxed by greedoids and extended by matroid intersection.
- **Canonical ordering by ratio**: sort items by a value to cost ratio before the greedy scan, at the price of a sort and a proof that the ratio orders correctly.
- **Local search**: move repeatedly to a better neighbour of the current solution until none exists, at the price of stopping at a local optimum.
- **Hill climbing**: step to an improving neighbour, either the best in the neighbourhood or the first one found, at the price of stalling on plateaus and local peaks.
- **Two-opt move**, also the **k-opt move**: remove k edges of a tour and reconnect them differently, at the price of a neighbourhood that grows with k.
- **Delta evaluation of a move**: score a move from the change it causes instead of rescoring the solution, at the price of maintaining incremental state.
- **List scheduling**: place each arriving job on the least loaded machine, longest jobs first when all lengths are known, at the price of a bounded gap from the optimal schedule.

### Bisection, sweeps, and precomputed ranges

- **Binary search on the answer**, also **bisection**: test a candidate answer with a monotone predicate and halve the range, at the price of one predicate evaluation per halving and a monotonicity proof.
- **Meet in the middle**, also **bidirectional search**: enumerate two halves separately and join their partial results, at the price of storing one half's whole enumeration.
- **Two pointers**: sweep two indices monotonically over a sequence in place of nested loops, at the price of requiring a monotone condition.
- **Sliding window**: maintain an aggregate over a moving contiguous range by incremental update, at the price of needing an invertible or monotone aggregate.
- **Monotonic stack**, also the **monotonic deque**: keep candidates ordered by value so the answer sits at one end, at the price of a single-direction sweep and queries confined to the current window.
- **Sweep line**, also **plane sweep**: process events in order along an axis while maintaining a status structure, at the price of sorting all events first.
- **Prefix sums**, also **cumulative sums**: precompute running totals so a range aggregate is one subtraction, extending to rectangles and to exclusive-or, at the price of a rebuild after any update.
- **Difference array**: record range updates as endpoint deltas and integrate once at the end, at the price of no queries before that integration.
- **Sparse table**: precompute overlapping power-of-two blocks for idempotent range queries, at the price of n log n memory and no support for updates.
- **Binary lifting**, also **jump pointers**: precompute power-of-two jumps so any distance is crossed in logarithmically many steps, at the price of n log n stored pointers.
- **Offline query processing**: read all queries first and reorder them for cheaper joint evaluation, at the price of giving up interactive answers.
- **Mo's algorithm**: order range queries by blocks so the window's total movement stays small, at the price of offline batching and a square root factor.
- **Small to large merging**, also the **smaller-half trick**: always merge the smaller structure into the larger one, at the price of an overall logarithmic factor.

### Pruning, bounding, and filtering

- **Backtracking**: extend a partial solution depth first and undo the last choice on failure, at the price of repeating work shared between branches.
- **Branch and bound**: prune any subtree whose bound cannot beat the incumbent, at the price of computing a bound at every node.
- **Constraint propagation**: narrow variable domains by enforcing constraints before searching deeper, from forward checking up to full arc consistency, at the price of propagation work at every node.
- **Variable ordering heuristic**, also **minimum remaining values**, also **VSIDS**: branch where failure comes soonest, on the smallest domain or on recently conflicting literals, at the price of maintaining the ranking statistics.
- **Conflict-driven clause learning**: derive a clause from each conflict so that region is never revisited, jumping back past assignments the conflict did not involve, at the price of a growing clause database.
- **Restart strategy**: abandon the current tree and start over while keeping learned facts, at the price of discarding the current partial search.
- **Symmetry breaking**: keep one member of each symmetric family of candidates, by added constraints or by canonical form deduplication, at the price of proving that some optimum survives.
- **Dominance pruning**: cut a branch or a state when another provably reaches an at least as good solution, at the price of proving the dominance relation.
- **Transposition table**: hash search states so their evaluations are reused across different paths, at the price of memory and collision risk.
- **Beam search**: keep only the best k nodes at each level of the search, at the price of discarding the branch holding the optimum.
- **Kernelization**: shrink an instance by answer-preserving reduction rules until only a core sized by the parameter remains, at the price of proving every rule safe.
- **Filter and refine**: shortlist candidates with a cheap filter then verify them exactly, at the price of false positives reaching the expensive stage.
- **Cheap test first**, also **predicate reordering**: evaluate the cheapest and most selective condition first, at the price of measuring selectivity.

### Adversarial and heuristic search

- **Minimax**, also **negamax**: evaluate a game tree assuming both players choose their best move, written as one recursion with negated returns, at the price of requiring a zero-sum evaluation.
- **Alpha-beta pruning**: skip branches that cannot change the minimax value, at the price of a strong dependence on move ordering.
- **Move ordering**: examine likely-best moves first so cutoffs happen early, ranking by moves that cut off at this depth or anywhere in the search, at the price of ordering work and tables per node.
- **Principal variation search**, also **NegaScout**: test non-first moves with a null window and re-search only on failure, at the price of occasional re-searches.
- **Futility pruning**: skip moves whose static score cannot reach the window, with razoring and late move reductions as the deeper cuts, at the price of unsound cuts near the horizon.
- **Monte Carlo tree search**, also **UCT**: grow the tree toward branches favoured by random playouts under a confidence bound, at the price of noisy estimates and a tuned exploration constant.
- **Retrograde analysis**, also the **endgame database**: classify positions backwards from terminal ones and store the results, at the price of storage for every classified position.
- **A star search**: order the frontier by path cost plus an admissible estimate of the remainder, at the price of memory linear in expanded nodes.
- **Admissible heuristic**: estimate that never exceeds the true remaining cost, and consistent when its change across an edge never exceeds that edge's cost.
- **Weighted A star**: inflate the heuristic to expand fewer nodes, at the price of a bounded loss of solution quality.
- **Pattern database**: precompute exact costs for a relaxed subproblem and use them as the heuristic, adding disjoint databases for a stronger bound, at the price of heavy precomputation and storage.

### Approximation and randomization

- **Approximation algorithm**: algorithm carrying a proved bound on how far its answer sits from the optimum.
- **Approximation scheme**, also **PTAS** and **FPTAS**: family reaching any fixed accuracy in polynomial time, fully polynomial when also polynomial in the inverse accuracy.
- **Rounding a relaxation**: solve a relaxed version and round its answer into a feasible one, treating fractional values as probabilities or fixing a few per round, at the price of the loss rounding introduces.
- **Primal-dual method**: grow a solution and a certificate together so the ratio follows, at the price of formulating and maintaining that certificate.
- **Scaling of input values**: round numbers to coarser units to shrink the state space, at the price of a controlled and bounded error.
- **Randomization**: make random choices so no input is systematically bad, always correct in the Las Vegas form and possibly wrong in the Monte Carlo form, at the price of guarantees only in expectation.
- **Randomized pivot selection**: choose the partition element at random, or shuffle the input first, to remove adversarial orders, at the price of losing any useful existing order.
- **Random sampling**: compute on a random subset and extrapolate to the whole, at the price of an error that shrinks only with sample size.
- **Random projection**: map high-dimensional points into fewer dimensions through a random matrix, at the price of distance distortion and a target dimension logarithmic in the point count.
- **Coreset**: keep a small weighted subset whose answer approximates the full input's, at the price of an approximation factor.

### String techniques that travel

- **Prefix function**, also the **failure function**: table of the longest proper prefix that is also a suffix, letting a scan resume without backtracking, at the price of pattern-sized preprocessing.
- **Rolling hash**, also the **Rabin-Karp technique**: update a window's hash in constant time as the window slides, so any substring's hash is derivable, at the price of verifying matches against collisions.
- **Bad character heuristic**, also the **good suffix heuristic**: skip ahead by the mismatched character's last occurrence or by the matched suffix's period, at the price of alphabet-sized and pattern-sized shift tables.
- **Shift-or technique**, also **bitap**: keep the set of active pattern prefixes in machine words and advance by shift and mask, at the price of patterns bounded by word width.
- **Suffix array**: sorted array of suffix offsets used where a suffix tree costs too much, built by prefix doubling or by induced sorting, at the price of auxiliary arrays for tree-shaped queries.
- **Banded alignment**: restrict the alignment matrix to a diagonal band, doubling the band until the answer fits inside it, at the price of repeated work and alignments whose gaps exceed the band.
- **Seed and extend**: find short exact matches then extend the promising ones, allowing don't-care positions inside the seed for sensitivity, at the price of missing matches that contain no seed.
- **Minimizer**, also **winnowing**: keep the smallest hash in each window as that window's representative, at the price of resolution lost between sampled positions.

### Geometry techniques that travel

- **Randomized incremental construction**: insert items in random order so expected structural change stays small, tracking which pending objects conflict with which built features, at the price of a shuffle and conflict lists.
- **Grid bucketing**: index objects by uniform cell so proximity queries scan neighbouring cells only, at the price of collapsing under nonuniform density.
- **Rotating calipers**: advance two supporting directions around a convex shape in one loop, at the price of requiring convexity.
- **Lifting transformation**: map points onto a paraboloid so proximity questions become convex hull questions, at the price of one added dimension.
- **Marriage before conquest**: discard the input that cannot contribute before recursing, so cost follows the output size, at the price of a selection step per level.
- **Well-separated pair decomposition**: represent all point pairs by few separated cluster pairs, at the price of a size blowup set by the separation parameter.
- **Floating-point filter**: evaluate a predicate in hardware arithmetic with an error bound and fall back to exact arithmetic when uncertain, at the price of two implementations.

### Graph decomposition and sparsification

- **Heavy-light decomposition**: cut tree paths into heavy chains so any path meets logarithmically many chains, at the price of chain bookkeeping over a range structure.
- **Centroid decomposition**: recurse on tree centroids so every path crosses a shallow separator, at the price of logarithmically nested auxiliary structures.
- **Euler tour technique**: flatten a tree into an array so each subtree becomes a contiguous range, at the price of doubling the array for edge-based queries.
- **Square root decomposition**: split the data into blocks of about square root size to balance update against query work, at the price of a square root factor in both and periodic rebuilds.
- **Tree decomposition**: reorganize a graph into bags of bounded width so dynamic programming states stay local, at the price of time exponential in the width.
- **Edge contraction**: merge an edge's endpoints into one vertex, contracting random edges when a cut must survive with useful probability, at the price of multiedges, lost identities, and repeated trials.
- **Spectral sparsification**: reweight a sparse edge subset that preserves every quadratic form, or every cut, within epsilon, at the price of approximate cut and flow values.
- **Contraction hierarchies**: precompute shortcuts in node importance order so a query only searches upward, as hub labels and region flags do with stored distances, at the price of heavy preprocessing per metric.
- **Augmenting path technique**: improve a solution along a path alternating between chosen and unchosen elements, saturating every shortest such path per phase, at the price of one search per unit of improvement.

### Storing answers against recomputing them

- **Precomputation**: compute reusable results before the queries arrive and read them from a table, at the price of setup time, storage, and staleness when the inputs change.
- **Rainbow table**, also the **Hellman table**: chained precomputed inversions of a function used to invert it online, at the price of large storage, false alarms, and chain re-evaluation per query.
- **Materialized view**: store a query's result as a physical table, at the price of storage and refresh work as base data changes.
- **Incremental view maintenance**: refresh a materialized view by applying only deltas, at the price of change tracking and maintenance logic.
- **Pre-aggregation**, also the **rollup table**: aggregate at write time rather than query time, at the price of a fixed grain and reprocessing for every new question.
- **Denormalization**: duplicate related fields into one table so joins disappear, at the price of storage and update anomalies.
- **Gradient checkpointing**, also **activation recomputation**: store a subset of intermediate results and recompute the rest, at the price of extra forward computation.
- **Lazy evaluation**: defer a computation until its value is demanded, at the price of thunk memory and unpredictable timing.
- **Incremental computation**, also **self-adjusting computation**: store dependency traces so only affected results recompute, at the price of trace memory and bookkeeping.
- **Dirty flagging**: recompute a derived value only when it is marked stale, at the price of flag state and the discipline to set it.
- **Floyd's cycle detection**, also **tortoise and hare**: detect repetition with two pointers instead of a visited set, at the price of traversing the sequence roughly twice.

### Caching read and write paths

- **Caching**: keep a copy of a result nearer its consumer, at the price of memory and the risk of serving stale data.
- **Cache-aside**, also **look-aside**: the caller reads the cache and fills it on a miss, at the price of duplicated fill logic and race windows.
- **Write-through**: write to cache and backing store together, at the price of write latency in exchange for a cache that never lies.
- **Write-back**, also **write-behind**: write to cache and flush later, at the price of durability risk and lost updates on failure.
- **Write combining**, also **write coalescing**: merge adjacent small writes into one larger write, at the price of a buffer and delayed visibility.
- **Cache invalidation**: remove entries when the source changes, by key, by tag, or by version, at the price of tracking which keys depend on which data.
- **Time to live expiry**: bound entry lifetime by a fixed age, checked on touch or swept on a timer, at the price of refetching entries that were still valid.
- **Stale-while-revalidate**: serve an expired entry while refreshing it in the background, at the price of bounded staleness for the first readers.
- **Request coalescing**, also **cache stampede prevention**: merge concurrent identical misses into a single origin call, at the price of shared latency and a pending-request map.
- **Prefetching**, also **read-ahead**: load data before it is requested, at the price of bandwidth and cache space whenever the prediction misses.
- **Content-hash fingerprinting**: name an asset by the hash of its bytes so it may be cached forever, at the price of rewriting every reference on change.

### Eviction and admission

- **Belady's optimal replacement**, also **MIN**: offline policy evicting the item used furthest in the future, the bound every real policy is measured against.
- **Least recently used**, also **LRU**: evict the entry untouched for longest, at the price of per-access bookkeeping and total collapse under one long scan.
- **Least frequently used**, also **LFU**: evict the least often used entry, decaying counts so old popularity fades, at the price of a counter per entry and a decay schedule to tune.
- **Second-chance**, also **CLOCK**: grant referenced entries one reprieve during a circular scan, at the price of only approximating recency.
- **Adaptive replacement cache**, also **ARC**: balance recency against frequency using hits on the keys of already evicted entries, at the price of doubled metadata.
- **TinyLFU**: admit a missed item only when a frequency sketch says it beats the victim, fronted by a small recency window, at the price of sketch memory and estimation error.
- **S3-FIFO**: filter one-hit wonders through small FIFO queues before the main cache, at the price of evicting slowly warming items early.
- **Cost-aware caching**: retain entries by recomputation cost divided by size rather than by recency, at the price of needing a trustworthy cost estimate.

### Compact, shared, and succinct representations

- **Succinct data structure**: representation near the information-theoretic minimum that still answers queries, compact within a constant factor and implicit when it holds no pointers, at the price of intricate code and slow constants.
- **Rank-select structure**: index over a bit vector answering rank and select in constant time, the primitive succinct trees and sequences are built from, at the price of lower-order extra space.
- **Wavelet tree**: hierarchy of bit vectors giving rank, select, and access over a sequence, at the price of a log-alphabet factor per query.
- **FM-index**: self-index over the Burrows-Wheeler transform counting occurrences by backward search, at the price of sampled positions to locate matches and block-sized construction memory.
- **Elias-Fano encoding**: monotone sequence stored as separated high and low bits, at the price of select machinery for random access.
- **Compressed sparse row**, also **CSR**: sparse matrix held as values, column indices, and row offsets, at the price of expensive structural modification.
- **Open addressing**: store entries in the table itself with no per-entry nodes, at the price of probe lengths that grow with load where chaining would spend a pointer instead.
- **Cuckoo hashing**: relocate keys among candidate slots to bound lookup probes, at the price of insertion failures and rehashes near capacity.
- **Interning**, also **hash consing**: keep one canonical copy of every distinct value so equality becomes pointer comparison, at the price of hashing at construction and a table that rarely releases memory.
- **Structural sharing**: let new versions reuse the unchanged parts of the old structure, copying only the path that changed, at the price of indirection and retained old nodes.
- **Copy-on-write**: share a representation until a writer forces a private copy, at the price of a check per write and latency spikes.
- **Deduplication**: store identical data once and reference it everywhere, cutting chunks at content-determined boundaries so edits shift few of them, at the price of a fingerprint index and fragmented reads.

### Bit-level and integer encodings

- **Bit packing**: store values in the fewest bits without respecting byte boundaries, at the price of shifting and masking on every access.
- **Word-level parallelism**, also **SWAR** and **broadword computing**: pack many small values into one machine word and operate on them together, at the price of masking to stop carries crossing lanes and code fixed to one word width.
- **Variable-length integer encoding**, also **varint**: spend fewer bytes on small numbers using continuation bits, with signs interleaved by zigzag, at the price of branchy byte-at-a-time decoding.
- **Frame of reference encoding**: store values as small offsets from a per-block reference, bit-packing the block and listing outliers as exceptions, at the price of block metadata and a patch pass on decode.
- **Delta encoding**: store differences between successive values, or gaps between sorted identifiers, at the price of sequential decoding and no random access.
- **Run-length encoding**: replace repetitions with a value and a count, at the price of expansion when the data does not repeat.
- **Dictionary encoding**: replace repeated values with short codes into a value dictionary, at the price of dictionary memory and an indirection per read.
- **Huffman coding**: optimal whole-bit prefix code derived from symbol frequencies, rebuilt at load from transmitted code lengths, at the price of a code table and wasted fractional bits.
- **Arithmetic coding**, also **range coding**: represent a whole message as one narrowed fraction, at the price of heavy arithmetic and no random access.
- **Asymmetric numeral systems**, also **ANS**: entropy coding through a single state and lookup tables, at the price of decoding in reverse order and a table per distribution.
- **LZ77**: replace repeats with references into a sliding window, at the price of window memory and match search time.
- **Quantization**: map stored values onto a coarse grid, per dimension or per subspace against a trained codebook, at the price of precision that cannot be recovered.

### Probabilistic structures and sketches

- **Bloom filter**: bit array with several hash functions testing set membership, at the price of false positives and no deletion.
- **Cuckoo filter**: store fingerprints in a cuckoo table so entries can be deleted, at the price of insertion failures near capacity.
- **XOR filter**: static membership structure smaller than a Bloom filter, at the price of an offline build holding every key and no updates afterwards.
- **Count-min sketch**: hashed counter rows estimating item frequencies, incrementing only the smallest counters to curb the error, at the price of overestimates under collisions.
- **HyperLogLog**: cardinality estimated from extreme patterns in hashed values, at the price of a fixed relative error and no element retrieval.
- **Locality-sensitive hashing**: hash so near neighbours collide and only a shortlist is compared exactly, at the price of missed neighbours and many parallel tables.
- **Quantile sketch**: bounded-size summary answering rank and quantile queries, by clustered centroids or by compacted levels, at the price of error concentrated where the summary is coarse.
- **Space-saving algorithm**: maintain a fixed set of heavy-hitter counters, admitting each new item over the weakest, at the price of overcounting newly admitted items.
- **Reservoir sampling**: maintain a uniform sample of a stream of unknown length in fixed space, at the price of answers derived from a sample.
- **Hierarchical navigable small world graph**: layered proximity graph searched greedily from sparse to dense layers, at the price of neighbour list memory and awkward deletion.

### Index and storage layout

- **Indexing**: build an auxiliary access structure so queries avoid a full scan, at the price of build time, storage, and maintenance on every write.
- **Inverted index**: map each term to the list of records containing it, with skip pointers for jumping within a list, at the price of storage and per-term update work.
- **Block-max WAND**: skip documents whose per-block score bound cannot enter the top k, at the price of storing a bound for every block.
- **Bitmap index**: one bit vector per distinct column value, held as arrays, bitmaps, or runs by container, at the price of space growing with cardinality.
- **Zone map**, also **min-max index**: per-block value ranges that let a scan skip whole blocks, at the price of no benefit once the data is unsorted.
- **Log-structured merge tree**: buffer writes in memory and merge sorted runs on disk, filtering runs that cannot hold a key, at the price of read amplification and compaction bandwidth.
- **B-tree fanout choice**: choose node size and branching factor, at the price of wasted page space when large or added depth when small.
- **Space-filling curve clustering**: interleave key bits so multidimensional neighbours are stored near each other, at the price of no single dimension being perfectly sorted.
- **Sharding**: split data across independent stores by hash or by key range, at the price of cross-shard queries, rebalancing work, and hotspots under skew.

### Parameterized and exponential-time techniques

- **Bounded search tree**, also **branch and reduce**: branch over a fixed set of repair options while the parameter drops, at the price of a tree exponential in the parameter.
- **Iterative compression**: grow the instance one element at a time, compressing an oversized solution back to size at each step, at the price of a compression routine per element.
- **Colour coding**, also **chromatic coding** and **random separation**: colour elements randomly so the sought structure's parts land in distinct colours, at the price of trials growing with the colour count.
- **Measure and conquer**: charge branches against a weighted measure of the instance so uneven branches are priced fairly, at the price of numerical weight tuning to reach the bound.
- **Cut and count**: count connected solutions modulo two by pairing consistent cuts, giving single-exponential treewidth algorithms, at the price of randomization and no witness returned.
- **Rank-based approach**: keep a basis of representative partitions in connectivity dynamic programming, the deterministic counterpart of cut and count, at the price of elimination work at every bag.
- **Important separators**: enumerate the bounded family of inclusion-maximal minimum separators and branch on them, at the price of exponential dependence on the separator size.
- **Crown decomposition**: expose an independent crown matched into a head so the crown reduces away, at the price of applying to covering problems only.
- **Nemhauser-Trotter reduction**: kernelize vertex cover to twice the optimum through a half-integral relaxation, at the price of solving that relaxation first.
- **Representative sets**: keep a small family preserving the extendability of every partial solution, at the price of matroid computations at every step.
- **Monotone local search**: turn an algorithm that extends a partial solution into a faster exponential algorithm for the whole problem, at the price of randomized subset sampling.
- **Protrusion replacement**, also **meta-kernelization**: swap a small equivalent gadget for a low-treewidth region with tiny boundary, at the price of replacement tables too large to tabulate.

### Satisfiability and constraint search

- **Unit propagation**, also **Boolean constraint propagation**: assign the last free literal of every one-literal clause and repeat to fixpoint, at the price of two-watched-literal state per clause.
- **Luby restart schedule**: draw restart lengths from a universal doubling sequence so no single run stalls the solver, at the price of many short early runs.
- **Phase saving**: reassign each variable the polarity it last held so a restart keeps the work below it, at the price of a stored phase per variable.
- **Clause database reduction**: delete learned clauses whose activity or literal block distance rates them unhelpful, at the price of relearning some of them later.
- **Bounded variable elimination**: resolve away variables whose removal does not grow the clause database, at the price of model reconstruction bookkeeping.
- **Blocked clause elimination**: delete clauses blocked on a literal, which preserves satisfiability, at the price of a witness stack for rebuilding models.
- **Incremental solving under assumptions**: reuse one solver across related queries by asserting unit assumptions, at the price of every permanent clause staying valid for all of them.
- **Maintaining arc consistency**: re-establish arc consistency at every search node, at the price of the heaviest propagation price per node.
- **Path consistency and bounds consistency**: the levels above and below arc consistency, over variable triples and over domain endpoints only, at the price of cubic work and of weaker pruning respectively.
- **Degree heuristic and least constraining value**: branch on the variable constraining most unassigned others, then try the value pruning fewest neighbours, at the price of degree counts and a neighbour lookahead.
- **Cube and conquer**: split a formula into cubes with a lookahead solver and hand each to a conflict-driven solver, at the price of unbalanced splits and coordination.
- **Lazy clause generation**: materialize a constraint's propagation as clauses on demand so the solver learns from it, at the price of memory for those clauses.
- **Dancing links**: thread doubly linked lists whose deletions undo exactly, making exact cover backtracking cheap, at the price of pointer-heavy memory traffic.

### Randomization and derandomization

- **Method of conditional expectations**: fix each random choice to the value that keeps the conditional expectation good, turning an existence proof into a construction, at the price of evaluating those expectations exactly.
- **Pairwise independence**, also **k-wise independent hashing**: draw from a family independent on k keys so concentration still holds on few random bits, at the price of weaker bounds than full independence.
- **Pessimistic estimator**: replace an intractable conditional failure probability with a computable upper bound during derandomization, at the price of a weaker guarantee than the random construction carries.
- **Randomized identity testing**, also **Freivalds' check**: test an algebraic identity by evaluating both sides at random points, at the price of a bounded chance of accepting a false identity.
- **Random weight isolation**: perturb weights randomly so the optimum becomes unique and can be read off, at the price of a wide weight range and a failure probability.
- **Epsilon-biased sample space**: enumerate a small distribution fooling every parity test in place of independent bits, at the price of guarantees only for parity-sensitive quantities.
- **Expander walk sampling**: draw correlated samples along a walk in an expander to spend few random bits, at the price of concentration weaker than independent sampling.
- **Nisan's space-bounded generator**: stretch a short seed into bits that fool small-space computation, at the price of a squared-logarithmic seed enumerated in full.

### Sketches and stream summaries

- **Theta sketch**: retain hashes below an adaptive threshold so sketches union, intersect, and difference, at the price of accuracy decaying across those set operations.
- **DDSketch**: bin values on a logarithmic scale so every quantile carries a relative error guarantee, at the price of bucket counts growing with the value range.
- **k-minimum values sketch**, also **bottom-k sketch**: keep the k smallest hashes and estimate cardinality from the largest kept, at the price of storing k full hashes.
- **Weighted reservoir sampling**: key each item by a weight-shaped random draw and keep the best keys, at the price of a priority queue over the sample.
- **Sticky sampling**: sample stream items at a falling rate to track frequent items within a bounded error, at the price of probabilistic guarantees only.
- **Count-mean-min sketch**: subtract estimated collision noise from each counter reading of a frequency sketch, at the price of estimates that can undershoot.
- **Flajolet-Martin sketch**, also **LogLog** and **SuperLogLog**: cardinality read from leading-zero or lowest-unset-bit patterns in hashed values, at the price of variance their harmonic-mean successors cut further.
- **Hierarchical heavy hitters**: track frequent items at every level of a key hierarchy with children discounted from parents, at the price of one summary per level.
- **Priority sampling and VarOpt sampling**: weight-based samplers giving unbiased subset sum estimates, VarOpt fixing the sample size, at the price of variance on small samples and intricate merge rules.
- **Smooth histogram**: keep overlapping sketch instances begun at chosen points so sliding-window answers stay accurate, at the price of several concurrent sketches.

### Repetition-aware text indexes

- **Grammar compression**, also the **straight-line program**: replace a text by a grammar deriving exactly it, the standard measure of repetitive compressibility, at the price of random access by tree descent.
- **Re-Pair**: repeatedly replace the most frequent symbol pair with a new nonterminal, at the price of a large auxiliary structure held during construction.
- **Relative Lempel-Ziv**: compress each sequence against a chosen reference sequence so extraction stays local, at the price of poor ratios when the reference is unrepresentative.
- **Prefix-free parsing**: cut text at content-defined triggers so a dictionary and parse index a huge repetitive collection, at the price of parameters tuned to repetitiveness.
- **LF mapping**: step from a position to its text predecessor through the compressed permutation, the primitive behind extraction and locating, at the price of a rank query per step.
- **Block tree**: point repeated blocks of a text at their earlier occurrences, at the price of a logarithmic factor on every access.
- **Range min-max tree**: navigate a balanced parenthesis sequence in constant time inside succinct space, at the price of intricate word-level operations.

## What the toolchain already does

### Constants, redundancy, and dead code

- **Constant folding**, also **constant-expression evaluation**: evaluates operations on literal operands at compile time and substitutes the result, at the price of reproducing the target's arithmetic and rounding exactly.
- **Constant propagation**, also **sparse conditional constant propagation**: replaces a variable's uses with the one constant it provably holds, the conditional form also marking branch edges infeasible so unreachable arms contribute nothing, at the price of a data flow pass and, across calls, whole module visibility.
- **Copy propagation**, also **forward propagation**: rewrites a use to name the value it was copied from, at the price of a longer live range for that value.
- **Correlated value propagation**: refines a value along one path using the conditions of dominating branches, at the price of dominator and predicate queries.
- **Global value numbering**, also **GVN**, also **common subexpression elimination**: numbers expressions proven to compute the same value and deletes the later ones, at the price of a temporary held live from the first computation to the last use.
- **Partial redundancy elimination**, also **PRE**, also **lazy code motion**: inserts a computation on the paths lacking it so a later one becomes fully redundant, at the price of code growth and evaluation on paths that formerly skipped it.
- **Load elimination**, also **store to load forwarding**: replaces a load with a value an earlier load or store already produced, at the price of dying at any possible pointer overlap and at any call whose writes the compiler cannot bound.
- **Predictive commoning**: keeps a value loaded in one iteration for the load that wants it in the next, at the price of registers holding carried values and a proof that nothing between them writes the location.
- **Store merging**, also **load widening**: fuses adjacent narrow accesses into one wider access, at the price of alignment assumptions and bytes touched that the program never named.
- **Dead code elimination**, also **DCE**, also **aggressive dead code elimination**: deletes instructions nothing reads, the aggressive form assuming everything dead until proven live so dead recurrences and branches go too, at the price of a control dependence analysis.
- **Dead store elimination**, also **DSE**: removes a store overwritten or unread before its location dies, at the price of stopping at every call the compiler cannot prove writes nothing reachable.
- **Loop deletion**, also **dead loop elimination**: removes a loop whose body leaves nothing live behind it, at the price of a termination proof, which the forward progress rule supplies for bodies without side effects.

### Algebraic and peephole rewriting

- **Algebraic simplification**: rewrites an expression by algebraic law into a cheaper equivalent and deletes identity and annihilating operands, at the price of laws that hold only for exact arithmetic.
- **Canonicalization**: rewrites equivalent forms into one representative and sorts commutative operands, so later passes need fewer patterns, at the price of a representative that is not always the cheapest form.
- **Instruction combining**, also **instcombine**, also **peephole optimization**: applies a catalog of local rewrites over a short window of instructions until nothing more matches, at the price of compile time and no view beyond the window.
- **Reassociation**, also **tree height reduction**: regroups associative operands to expose constants and to shorten dependence chains, at the price of a changed evaluation order, which floating point forbids until relaxation permits it.
- **Integer narrowing**, also **sign extension elimination**: performs an operation in the narrowest type holding every possible result and drops extensions whose bits no consumer demands, at the price of a value range proof.
- **Division by invariant multiplication**, also **magic number division**: replaces division by a constant with a widening multiply, a shift, and a correction, and derives the remainder from the quotient, at the price of several instructions per distinct divisor.
- **Multiplication by constant expansion**: replaces a multiply by a constant with shifts, adds, and subtracts, at the price of instruction count once the constant has many set bits.
- **Machine idiom recognition**: matches a written-out sequence onto one instruction, covering byte swap, rotate, bit field insert, population count, leading zero count, saturating and averaging arithmetic, and widening dot product, at the price of firing only on the exact shape it knows and of undefined behaviour where the hand-written form was more defined than the instruction.
- **Library call simplification**: folds a call to a known standard routine into cheaper code, a constant, or a vector implementation, at the price of assuming the library keeps standard semantics, standard accuracy, and standard error reporting.
- **Superoptimization**, also **stochastic superoptimization**: searches the space of instruction sequences for the cheapest one meeting a specification, at the price of search time far beyond any normal pipeline and confidence resting on equivalence testing.

### Memory, aggregates, and code motion

- **Promotion of memory to registers**, also **mem2reg**: converts loads and stores of a stack slot into SSA values, at the price of firing only while that slot's address never escapes.
- **Scalar replacement of aggregates**, also **SROA**: splits a local aggregate into independent scalars that live in registers, at the price of firing only while the aggregate is never passed, stored, or copied whole.
- **Register promotion**: replaces repeated loads and stores of one location with a register plus a single load and store, at the price of a proof that no aliasing access observes the intermediate values.
- **Memory copy optimization**, also **memcpyopt**: turns store sequences and copy pairs into one library copy or removes the copy entirely, at the price of proving that source and destination cannot overlap.
- **Stack allocation of non-escaping objects**: places a provably local allocation in the frame and replaces its fields with scalars, at the price of an escape proof that one stored reference destroys.
- **Loop invariant code motion**, also **LICM**: moves computations whose operands never change into the preheader, at the price of executing them on zero-iteration entries and holding them live across the whole loop.
- **Loop invariant store motion**, also **store sinking**: lifts a store with unchanging address out of the loop and writes once at the exit, at the price of a window in which memory is stale and a proof that no other access reads it there.
- **Code hoisting and sinking**: moves value-equal expressions up into a common dominator or down to the successor that consumes them, at the price of speculative execution one way and duplicated copies the other.
- **Partial dead code elimination**: sinks an assignment past the branch on which it is dead, at the price of duplicating it into the paths that keep it.
- **Load speculation**: hoists a load above a branch once its address is known dereferenceable, at the price of memory traffic on paths that never needed the value.
- **Down safety**, also **up safety**: the conditions that a computation placed at a point is used on every path leaving it, and that it is already available on every path reaching it, which together bound where any code motion may put it.

### Control flow and predication

- **Control flow graph simplification**, also **simplifycfg**: merges, straightens, and deletes blocks and folds branches whose successors are identical or whose condition is known, at the price of invalidating analyses every time it runs.
- **Unreachable code elimination**: deletes blocks no path from entry reaches, at the price of a reachability traversal after every control flow change.
- **Jump threading**: sends a branch whose outcome one incoming path already settles straight to its target, at the price of duplicating the blocks along that path.
- **Tail merging**, also **cross-jumping**: replaces identical instruction sequences ending several blocks with one shared copy, at the price of an added branch and lost fall-through.
- **If-conversion**, also **predication**: replaces a branch with predicated or selected computation on both paths, conditional moves and branchless minimum and maximum being its smallest forms, at the price of issue slots spent on work the taken path discards.
- **Switch lowering**: expands a multiway branch into a mixture of comparison chains, jump tables, bit tests, and constant lookup tables, at the price of table space or branch depth chosen per switch.
- **Trace and superblock formation**, also **hyperblock formation**: builds a single-entry region along a likely path, by duplicating tails or if-converting the alternatives, so later passes see straight-line code, at the price of code growth and compensation code off the trace.
- **Tail call optimization**, also **sibling call optimization**: reuses the current frame for a call in tail position, at the price of the caller's frame vanishing from stack traces, profiles, and security frame walks.
- **Zero cost exception handling**, also **table driven unwinding**: moves dispatch data into side tables so the non-throwing path executes no extra instruction, at the price of large tables and slow throws.
- **Invoke to call conversion**: rewrites a call proven not to throw into its plain form and deletes the cleanup structure around it, at the price of resting on nothrow inference through every callee it reaches.

### Laziness, closures, and unboxing

- **Let floating**, also **full laziness**: moves a binding outward past enclosing binders so its value is computed once and shared, at the price of keeping that value alive far longer than the code using it.
- **Worker wrapper transformation**: splits a function into a strict unboxed worker and a small inlinable wrapper, at the price of code size and total reliance on the wrapper being inlined.
- **Unboxing**, also **strict field unpacking**: represents a strict value or constructor field in raw machine form instead of a heap box, at the price of lost sharing and copying at construction.
- **Case of case transformation**: pushes an outer case into the branches of an inner one so scrutinee constructors become known, at the price of duplicating the outer alternatives.
- **Call pattern specialization**, also **SpecConstr**: clones a recursive function for each constructor pattern its own recursive calls supply, at the price of code size proportional to the pattern count.
- **Dictionary specialization**, also **type class specialization**: clones an overloaded function at a concrete instance so dictionary indirection disappears, at the price of one body per instantiation and tighter recompilation coupling between modules.
- **Lambda lifting**: replaces a local function's free variables with parameters so it needs no closure, at the price of longer argument lists and register pressure at every call.
- **Join point**, also **loopification**: compiles a local continuation that is only ever tail called as a jump rather than a closure, at the price of the distinct frame a debugger would have shown.
- **Stream fusion**, also **foldr build fusion**: deletes an intermediate sequence by pairing a producer with a consumer, at the price of requiring both sides in fusible form and aggressive simplification afterwards.

### The analyses, which change nothing

- **Alias analysis**: decides whether two references can address the same location, answering must, may, or no, and every memory transformation consults it before moving anything.
- **Points-to analysis**: computes the abstract objects each pointer may hold, inclusion-based solving giving precision at cubic cost and unification-based solving near-linear time at coarser precision.
- **Analysis sensitivity**: the dimensions along which a result is split or merged, namely flow, context, field, and object sensitivity, each trading precision against the size of the result and the time to reach it.
- **Escape analysis**, also **capture tracking**: determines whether a reference can leave its creating scope, its thread, or a callee it was passed to, which is the precondition every allocation removal rests on.
- **Modification and reference analysis**, also **mod-ref analysis**: records which locations each statement or call may read or write, and proves functions pure or free of memory access altogether.
- **Data flow analysis**: derives facts at every program point by propagating them along edges to a fixed point in a lattice of monotone transfer functions, with widening forcing convergence in tall domains and the computed solution being no more precise than the ideal meet over all paths.
- **The classical data flow problems**: reaching definitions, live variables, available expressions, and very busy expressions, whose partial and anticipable forms are exactly what redundancy elimination and code motion consume.
- **Dominance and control dependence**: the relations naming which blocks every path must pass through and which branch decides whether a statement runs, with dominance frontiers giving minimal merge placement.
- **Value fact analyses**: range, known bits, demanded bits, nullness, and alignment analyses, each supplying the single fact that licenses a narrowing, a removed check, or a wider access.
- **Scalar evolution analysis**, also **chains of recurrences**: describes a value's change across iterations as a recurrence, yielding strides, trip counts, and closed forms for values after the loop.
- **Call graph construction**: builds which procedures may call which, class hierarchy analysis bounding a virtual call by the declared receiver's subtypes and rapid type analysis narrowing to classes the program actually instantiates.
- **Divergence analysis**, also **uniformity analysis**: determines which values are identical across all threads of a parallel execution, so scalar registers and uniform branches may be used for them.

### What the source promises

- **Undefined behaviour based simplification**: assumes an execution containing undefined behaviour never happens, so the code around it simplifies, at the price of surprising outcomes in programs that contain it.
- **Strict aliasing exploitation**: assumes accesses through incompatible types never overlap, at the price of miscompiling code that reinterprets memory through a cast, including across a call once the rule is applied interprocedurally.
- **Signed overflow assumption**, also **no-wrap flag exploitation**: assumes signed arithmetic never wraps so counters widen and comparisons fold, at the price of programs that rely on wrapping.
- **Restrict qualification**: promises a pointer's target is reached through no other pointer, which is what lets loads and stores move past each other, at the price of undefined behaviour when the promise fails.
- **Non-null and dereferenceable attributes**: promise a pointer is never null and addresses a stated number of readable bytes, so null tests fold and loads may be speculated, at the price of faults when either claim is untrue.
- **Alignment assumption**: promises an address meets a stated alignment so wider and faster accesses become legal, at the price of faults or slow paths on misaligned data.
- **Pure and const attributes**: declare that a result depends only on the arguments and, in the const case, that the function reads no memory, so calls may be shared, hoisted, or deleted, at the price of a declaration that must be true and of every unproven call blocking the transformations around it.
- **Likely and unlikely hints**: annotate an outcome as probable so layout, speculation, and inlining follow it, at the price of worse code on the other path and of hints that outlive their accuracy.
- **Fast math relaxation**: permits contraction, reassociation, reciprocal approximation, and the absence of infinities, not-a-numbers, and signed zeros, at the price of reproducible rounding and worst-case accuracy.
- **Forward progress assumption**, also **finite loop assumption**: assumes a loop without side effects terminates so it may be deleted or moved, at the price of miscompiling code that spins deliberately.
- **Data race freedom assumption**: optimizes as though no data race exists, so a shared load may be cached in a register across the whole loop, at the price of unbounded behaviour in racy code.
- **Volatile access preservation**: forbids the removal, duplication, or reordering of accesses marked volatile, at the price of blocking every optimization through them.

### Loop restructuring

- **Loop rotation**, also **loop inversion**: moves the exit test to the bottom of the loop and guards entry with a zero trip test, at the price of a duplicated condition.
- **Loop unrolling**, also **unroll and jam**: replicates the body so branch and counter overhead is paid once per group and independent copies expose parallelism, the jam form fusing the inner copies of an unrolled outer loop, at the price of code size, instruction cache pressure, register pressure, and a remainder loop when the trip count does not divide.
- **Loop peeling**, also **index set splitting**: pulls boundary iterations or a subrange out so a guard or subscript inside the remaining loop becomes uniform, at the price of duplicated body text.
- **Loop unswitching**: hoists a loop-invariant condition out and keeps a specialized loop per outcome, at the price of doubling the loop's code.
- **Loop fusion**, also **loop jamming**: merges adjacent loops over the same range so shared arrays are reused in registers, at the price of register pressure and a proof that no dependence between the loops reverses.
- **Loop distribution**, also **loop fission**: splits one body into separate loops over the same range so dependence cycles are isolated and idioms exposed, at the price of repeated traversal and lost reuse.
- **Loop interchange**, also **loop permutation**: reorders levels of a nest to shorten stride or move a parallel level outward, reversal and skewing composing with it as one integer matrix, at the price of legality read from the transformed distance vectors.
- **Loop versioning**: emits a specialized loop plus a runtime test selecting it, the test comparing pointer ranges, alignment residues, or trip count, at the price of two bodies and check overhead that short loops never repay.
- **Induction variable simplification**: canonicalizes counters onto one zero-based variable, widens them to pointer width, substitutes closed forms, and rewrites the exit test so the original counter dies, at the price of an argument that the counter cannot wrap.
- **Loop strength reduction**: replaces multiplication by the index with an addition carried between iterations and folds the result into the target's cheapest addressing form, at the price of an extra live register per reduced expression.
- **Loop idiom recognition**: matches a whole loop onto a fill, copy, population count, or leading zero count primitive, at the price of brittle matching and of per-element side effect order the primitive does not keep.
- **Reduction recognition**: identifies an accumulation through an associative operator so it can be split into private partial results or a tree, at the price of a summation order that changes floating point results.
- **Scalar expansion and privatization**: gives each iteration or thread its own copy of a variable so dependences arising from storage reuse vanish, at the price of memory proportional to the iteration space and of copy in and copy out code at the boundaries.

### Tiling and locality

- **Loop tiling**, also **blocking**, also **strip mining**: divides the iteration space into tiles run one at a time so each working set fits a memory level, register, cache, and translation buffer tilings nesting inside one another and extents chosen from capacity and reuse estimates, at the price of extra loop levels and tuning that does not carry to another machine.
- **Loop skewing**, also **time skewing**: adds a multiple of an outer index to an inner one so dependences become uniform and a time-iterated nest becomes tilable, at the price of trapezoidal bounds and thin parallelism at the edges.
- **Overlapped and diamond tiling**: shapes tiles so neighbours need no exchange, or so concurrent start survives at every time step, at the price of redundantly computed halo points or intricate generated bounds.
- **Data copying**, also **copy optimization**: copies each tile into a contiguous buffer before the tiled loops read it, at the price of copy time and buffer memory.
- **Array transposition**, also **array of structures to structure of arrays**: permutes dimensions or splits fields into separate arrays so the inner loop walks with unit stride, at the price of rewriting every access and of every other traversal getting worse.
- **Software prefetch insertion**: issues prefetches for addresses some iterations ahead, following an indirection when the pattern demands, at the price of instruction slots, bandwidth, and a distance constant tied to one machine's latency.
- **Non temporal store insertion**, also **streaming store**: writes data with no reuse past the cache hierarchy, at the price of hurting any later reader that would have hit.
- **The polyhedral model**: represents statement instances as integer points of parameterized polyhedra, with affine schedules giving order and access relations giving the elements each instance touches.
- **Affine scheduling**, also **the tiling hyperplane method**: solves the dependence constraints for a schedule that keeps distances nonnegative and short so bands become tilable and reuse stays local, at the price of a linear program growing with program size and of code generation whose bounds are complex.

### Dependence and its tests

- **Data dependence analysis**: decides for each pair of references whether two iterations touch the same location, and labels each dependence with its kind, its level, and its distance.
- **Distance and direction vectors**: the component-wise difference of two iteration vectors and the signs of that difference, whose lexicographic positivity after a transformation is the general legality test for every reordering.
- **True, anti, and output dependence**: a read after a write that carries a value, and the write-after-read and write-after-write orders that exist only because storage is reused and that expansion or renaming removes.
- **Loop carried dependence**: a dependence whose endpoints lie in different iterations, whose absence makes a loop a DOALL loop and whose cycles force the statements they contain to run in order.
- **Subscript classification**: the split into subscripts with no loop index, one index, or several, and into coupled groups that must be tested together, which decides which dependence test can apply at all.
- **The dependence tests**: the greatest common divisor and Banerjee tests, which ignore or relax the loop bounds, the closed-form single-index and delta tests, and the exact Omega test, cost rising with each step toward exactness.
- **Memory disambiguation**: establishes that two references cannot address the same storage, at the price of imprecision wherever pointer arithmetic, unknown bounds, or a subscript computed through another array hides the shape.
- **Delinearization**: recovers multidimensional subscripts from a flattened address expression so array tests apply, at the price of resting on bound assumptions it cannot prove.
- **Safe vectorization distance**, also **safelen**: the smallest distance a loop carries, which caps the vector length or unroll factor any transformation may legally use.

### Vectorization and masking

- **Vectorization**, also **autovectorization**: rewrites element-wise scalar work as operations on vectors, the innermost loop strip mined to the vector width, at the price of legality proofs, remainder handling, and packing overhead that small trip counts never repay.
- **Superword level parallelism**, also **SLP**, also **basic block vectorization**: packs isomorphic scalar statements inside one block into vector operations, at the price of pack and extract shuffles at the boundaries of the packed region.
- **Vectorization cost model**: compares a modelled vector plan against the scalar loop in issue slots, latency, or emitted bytes, and refuses any loop below the break-even trip count or needing more runtime checks than its budget allows, at the price of decisions only as good as the model and a plan chosen before a single instruction is emitted.
- **Tail folding**, also **tail predication**: runs the remainder iterations inside the main vector body under a lane mask, at the price of masked memory operations that the target must provide.
- **Alignment peeling**: peels iterations until the leading reference reaches a vector boundary, at the price of a scalar prologue whose length is unknown until the loop runs.
- **Masked vector operations**: apply a lane mask so inactive lanes leave their destination and memory untouched, an active lane mask derived from the counter and trip count covering the final iteration, at the price of mask computation and hardware support.
- **Gather and scatter vectorization**: uses indexed vector loads and stores where subscripts are themselves arrays, structured and permuting forms handling interleaved fields and constant strides instead, at the price of per-lane memory latency and bandwidth spent on elements no lane uses.
- **Scalable vectorization**: emits code for a width unknown until execution so one binary serves every width, at the price of predicate-driven control, configuration instructions before each region, and no compile-time trip count folding.
- **Whole function vectorization**, also **elemental function**: compiles a function to accept vectors of argument sets so vector loops may call it, uniform and linear declarations keeping chosen parameters scalar or contiguous, at the price of a second code path and unsoundness when those declarations do not hold.
- **Vector reduction**: keeps a vector of partial accumulators and folds the lanes afterwards, ordered forms preserving the original association and histogram forms serializing conflicting indices through conflict detection, at the price of a changed summation order in every form but the ordered one.

### Pipelining and iteration parallelism

- **Software pipelining**, also **modulo scheduling**: overlaps successive iterations in a kernel scheduled at a fixed initiation interval, iterative and swing variants retrying at wider intervals or ordering by criticality, at the price of prologue and epilogue code, register pressure, and outright failure when resources conflict.
- **Initiation interval**: the cycles between the starts of consecutive iterations, bounded below by the busiest functional unit and by the longest dependence cycle divided by the distance it spans.
- **Modulo variable expansion**: unrolls the kernel until overlapping lifetimes of one value receive distinct registers, hardware register rotation removing the need entirely, at the price of kernel code size.
- **Auto parallelization**: spreads a loop's iterations across threads with no annotation in the source, at the price of conservative analysis and threading overhead that swamps small loops.
- **DOACROSS parallelization**: keeps carried dependences and enforces them with point to point synchronization rather than serializing the loop, at the price of synchronization latency on the critical path.
- **Loop scheduling policies**: static, cyclic, block cyclic, dynamic, guided, factoring, and work stealing assignment of iterations to threads, at the price of scheduling overhead and lost data locality in exactly the policies that balance best.
- **Speculative loop parallelization**, also **thread level speculation**: runs iterations in parallel while checking for violated dependences and rolling back on conflict, at the price of checkpoints and work thrown away.
- **Offload region formation**: outlines a nest as an accelerator kernel, collapsing the iteration space onto a thread grid, staging tiles in scratchpad, and coarsening work items to fit a register budget, at the price of transfer and launch latency, explicit barriers, and spills to slow memory when occupancy is pushed.

### Instruction selection and scheduling

- **Instruction selection**: maps intermediate operations onto machine instructions by greedy or optimal tree covering, by covering a graph so shared subexpressions match once, or over a whole function, at the price of a search space no local rule covers optimally.
- **Instruction legalization**: rewrites operations and types the target cannot encode into supported equivalents, expanding to a library call where nothing matches, at the price of code growth and call overhead.
- **Addressing mode selection**: folds scaled index arithmetic, displacements, and pointer bumps into the memory operand itself, at the price of recomputation when the address is reused and of scheduling constrained by auto-increment forms.
- **Fused operation selection**: matches a multiply feeding an add, two adjacent accesses, or a decoder-fusible pair onto one instruction, at the price of altered floating point rounding and tuning that helps one microarchitecture.
- **Instruction scheduling**: reorders instructions to respect dependences while hiding latency, driven by a machine model of functional units, issue width, and hazards, at the price of more values live at once.
- **Prepass and postpass scheduling**: schedules before allocation on virtual registers or after it on physical ones, at the price of demanding more registers than exist in the first case and inheriting false dependences from register reuse in the second.
- **Trace and superblock scheduling**: schedules a likely path as one region, at the price of compensation code on every edge that leaves or joins the trace.
- **Speculative code motion**: hoists an operation above a branch that may not reach it, boosting and sentinel forms adding recovery code or a deferred fault check, at the price of wasted work and the metadata to undo it.
- **Bundling and delay slot filling**: packs independent operations into a wide issue bundle or into the slots following a branch, at the price of padding when slots stay empty and correctness reasoning on both branch paths.
- **Atomic and barrier lowering**: builds an unsupported atomic operation from a reservation or compare and swap retry loop and picks the weakest machine fence implementing the language's ordering, at the price of livelock risk under contention and miscompilation when the mapping is misread.

### Registers, frames, and layout

- **Register allocation**: assigns unlimited virtual registers to a finite file, by coloring an interference graph, by one scan over live intervals, or by greedy assignment with eviction and splitting, at the price of memory traffic wherever demand exceeds supply and of a problem solved only heuristically.
- **Spilling**: stores a value to a stack slot and reloads it at each use, candidates ranked by use frequency and loop depth and placed where paths are coldest, at the price of memory traffic wherever that ranking is wrong.
- **Rematerialization**: recomputes a cheap value at its use instead of reloading it, at the price of applying only to operations with no side effects and no memory read that could have changed.
- **Register coalescing**: merges the two ends of a copy into one live range so the copy disappears, aggressive forms merging regardless of the resulting degree, at the price of a range that may no longer color.
- **Phi elimination**: replaces merge nodes with copies on incoming edges, sequentializing parallel copies through a scratch register and splitting critical edges to give them a home, at the price of copies the coalescer must then remove.
- **Callee-save and caller-save assignment**: decides which values live in registers preserved across calls, shrink wrapping moving each save into the paths that actually need it, at the price of several save sequences and more intricate unwind data.
- **Frame pointer omission**: frees the frame pointer for general use and reaches locals through the stack pointer, at the price of unwinding, profiling, and debugging that relied on the frame chain.
- **Basic block reordering**: places blocks so the likely successor falls through, chains built by repeatedly merging the heaviest control edge, at the price of unconditional branches on the displaced paths and dependence on a representative workload.
- **Hot and cold splitting**: moves rarely executed blocks into a separate section or an outlined function so the hot body stays compact, at the price of a long branch or a call whenever the cold path does run.
- **Branch relaxation**: widens a branch whose displacement no longer reaches its target, inserting a range extension thunk where no encoding suffices, at the price of growth that can force further widening.
- **Hardening lowering**: emits stack canaries, shadow stacks, indirect branch thunks, pointer authentication, indirect call type checks, and initialization of locals the program left uninitialized, at the price of instructions on every protected call and function, whole program type information for the call checks, and large slowdowns where loads are hardened against misspeculation.

### Whole program and link time

- **Inlining**, also **procedure integration**: replaces a call with the callee's body so the code specializes to that site, decided by a cost model over size, frequency, and expected simplification, partial forms inlining only a cheap early exit, at the price of code size, compile time, and growth concentrated wherever the estimate is wrong.
- **Interprocedural constant propagation**: carries constant arguments, return values, known bits, and value ranges across the call graph, cloning a callee where distinct call sites supply distinct constants, at the price of whole program visibility, code growth per clone, and recompilation coupling between units.
- **Function attribute inference**: deduces read-only, no-unwind, no-alias, pure, and const attributes from bodies so calls stop blocking the transformations around them, at the price of a fixed point over the call graph and unsoundness once a callee can be replaced at run time.
- **Internalization**: gives a symbol local linkage once nothing outside is proven to reference it, which is what licenses the aggressive passes that follow, at the price of correctness if a new consumer appears at run time.
- **Whole program devirtualization**: replaces a virtual call with a direct one after enumerating every implementation in the program, and deletes virtual table entries no live site can reach, at the price of a closed world that dynamic loading and reflection break.
- **Link time optimization**, also **LTO**, also **whole program optimization**, also **cross module optimization**: defers code generation to the link so modules optimize together, the monolithic form merging everything into one program and the thin form linking summaries then compiling modules in parallel with imported bodies under an import budget, at the price of build time, memory, and lost incremental rebuilds.
- **Linker garbage collection of sections**: discards sections no live symbol reaches, at the price of per-function sections and roots that must all be declared.
- **Identical code folding**: merges functions whose bodies or emitted bytes match onto one symbol, at the price of function addresses that are no longer distinct, which some programs compare.
- **Semantic interposition suppression**: assumes a defined global function is not replaced at load time so its calls may be inlined, at the price of preloading and interposition ceasing to work.
- **Position independent access cost**: the table load reaching a global and the stub traversed by a call the dynamic loader resolves, reduced by hidden visibility, direct call promotion, and immediate rather than lazy binding, at the price of symbols becoming unavailable to other modules and startup work for symbols never used.
- **Post link optimization**: rewrites and relays out a linked binary from a sample profile of that binary, at the price of preserved relocations, rebuilt unwind tables, and control flow the tool must recover heuristically.

### Profile-guided optimization

- **Profile guided optimization**, also **feedback directed optimization**: drives layout, inlining, unrolling, spill placement, devirtualization, and size policy from measured behaviour, at the price of a training run whose resemblance to production bounds every gain it can deliver.
- **Instrumentation based profiling**: inserts counters to record exact frequencies, minimal placement instrumenting only edges outside a spanning tree and deriving the rest, at the price of a large slowdown in the instrumented build.
- **Sampling based profiling**, also **AutoFDO**: derives frequencies from periodic hardware samples of an optimized binary and maps them back to source positions, at the price of noisy counts and attribution error where the optimizer moved code.
- **Static profile estimation**: predicts branch outcomes from structural heuristics such as loop back edges, pointer comparisons, and guarded returns, then propagates block frequencies through the loop structure, at the price of frequent misprediction on unusual code.
- **Value profiling**: records the distribution one runtime value takes so its common case can be specialized behind a guard, at the price of per-site histogram overhead during training and a fallback path afterwards.
- **Indirect call target profiling**: records which functions an indirect call actually reaches so it becomes a guarded direct call, at the price of a check on every execution and a mispredicted fallback when the target shifts.
- **Profile staleness**: the decay of a profile as the code changes, matched back onto moved and renamed functions by structural hashes, whose failure shows up as counts attributed to the wrong code.

### Tiering, warmup, and runtime compilation

- **Just in time compilation**: compiles during execution so observed types, values, and frequencies inform the code, where ahead of time compilation has none of them, at the price of compilation time charged against the running program.
- **Tiered compilation**: routes code through progressively more expensive compilers as it heats, a baseline compiler emitting native code immediately and an optimizing tier following, at the price of several versions of every hot method and the machinery to move between them.
- **Invocation and backedge counters**: per-method and per-loop tallies whose thresholds trigger compilation, the backedge counter catching a long-running loop without waiting for the method to be entered again.
- **Compilation policy**: the queue, the budget, and the choice between compiling in the background and blocking the calling thread, at the price of application processor time in one case and a visible latency spike in the other.
- **On stack replacement**, also **OSR**: replaces the code of an executing frame in place so a running loop moves to a better tier, at the price of mapping state between the two versions at the transfer point.
- **Tier down**, also **reprofiling**: returns invalidated or cooled code to a counting tier so fresh information accumulates, at the price of running slow code again while it reheats.
- **Trace based compilation**: compiles a recorded linear path straight through call boundaries, side exits leaving to the interpreter or stitching to another trace, at the price of guard-heavy code and traces multiplying with the paths through the loop.
- **Code cache**: the runtime-managed memory holding compiled code, stubs, and metadata, swept and flushed to reclaim space, at the price of recompiling evicted methods and of usable memory lost to fragmentation between live bodies.
- **Warmup**: the interval in which a runtime is still profiling and compiling and has not reached steady performance, which is what every choice between startup latency and peak throughput trades against.
- **Persisted profile**, also **warmup profile replay**: carries a profile from earlier runs into a later startup so the optimizing tier begins hot, at the price of storage and of stale decisions when the workload shifts.
- **Adaptive specializing interpreter**: counts executions per instruction and rewrites hot ones in place into specialized forms, quickening operands once resolved and joining frequent sequences into one handler, at the price of counters, specialization metadata, and a path back to the general form.

### Speculation, guards, and deoptimization

- **Speculative optimization**: compiles code correct only under the conditions observed so far, with a fallback when they fail, at the price of guards on the fast path and metadata at every point where it can leave.
- **Guard insertion**: emits the runtime check that a speculated assumption still holds, strengthened into one earlier check or hoisted out of a loop so it covers many, at the price of failing on inputs the weaker or later check would have accepted.
- **Deoptimization**, also **dynamic deoptimization**, also **uncommon trap**: abandons speculative code and reconstructs interpreter state at the failure point, at the price of a frame state record at every such point, whose size grows with every speculation taken.
- **Uncommon trap**, also **uncommon branch pruning**: emits no code at all for a path the profile never took and traps into the runtime instead, at the price of a full deoptimization the first time that path is taken.
- **Assumption tracking**, also **dependency recording**: registers each fact a compilation relied on so that fact's violation can invalidate the code, at the price of tracking every dependency taken.
- **Code invalidation**: patches or discards compiled code whose assumptions no longer hold, barring new entries while existing activations finish, at the price of two versions of the method live at once.
- **Failed speculation record**: a per-method record of which speculations have already failed, so recompilation does not repeat them and the method stops cycling between speculation and deoptimization.
- **Type feedback and type specialization**: records the concrete types a site has received and compiles for exactly those, at the price of deoptimization the moment a new type arrives.
- **Value speculation**: assumes a loaded or returned value equals one previously observed, fields declared stable or provably immutable being folded outright, at the price of a compare on every use and invalidation if the field is written again.
- **Speculative inlining**: inlines the target the profile favours behind a guard, polymorphic forms inlining several observed targets behind a type dispatch, at the price of code size multiplied by target count and a fallback call on mismatch.
- **Class hierarchy analysis in a runtime**: proves a method has a single implementation among the currently loaded classes so its calls become direct, at the price of invalidation whenever a class is loaded.
- **Range check elimination in a runtime**: proves an index within bounds from the loop's structure and drops the check, loop predication turning a loop-invariant check into one test before the loop, at the price of deoptimizing the entire loop when that one test fails.
- **Implicit null check**: relies on the hardware fault of the access itself instead of an explicit test, at the price of a signal handler, mapped guard pages, and a precise mapping from fault address back to program point.

### Inline caches, shapes, and runtime memory

- **Inline cache**: caches a dynamic call's resolved target at the call site so later executions skip the lookup, at the price of a guard on every call and code that must be patchable.
- **Polymorphic inline cache**: caches several receiver shapes and their targets at one site as a short dispatch chain, at the price of a check per entry and a fall back to full lookup once the site has seen too many shapes.
- **Hidden class**, also **shape**, also **map**: the runtime descriptor that gives a dynamic object a fixed field layout, transitions on property addition forming a tree that objects built the same way reuse.
- **Property access specialization**: compiles a field read or write to a fixed slot offset behind a shape check, at the price of deoptimization on layout change and of falling back to hash storage once an object's shape churns.
- **Unboxing in a runtime**: keeps a numeric value in a machine register rather than a heap object, at the price of boxing again at every boundary the value escapes through.
- **Partial escape analysis**: removes an allocation on the paths where it does not escape and materializes the object only where it does, at the price of duplicated code and objects rebuilt at every deoptimization point that exposes them.
- **Allocation inlining**: emits a bump pointer sequence inline with a slow path call, each thread bumping within its own allocation buffer, at the price of code size at every allocation site and wasted tail space per buffer.
- **Safepoint polling**: inserts the checks at which a thread can be brought to a known state, and elides them from short counted loops, at the price of a poll on backedges and returns, or of longer latency before a thread can be paused.
- **Stack map**, also **oop map**: the per-safepoint table naming which registers and frame slots hold references, which lets a collector find roots precisely instead of scanning every word that might be a pointer.
- **Collector barriers**: the write barrier recording a modified reference for the collector and the load barrier checking and repairing every reference read so relocation can proceed concurrently, elided where a store cannot create a tracked reference and coalesced across writes to one object, at the price of instructions on the program's hottest operations and a staler remembered set.
- **Lock elision and coarsening**: removes synchronization on an object proven unshared and merges adjacent lock regions on one object, licensed by the rule that operations may move into a synchronized region but never out of one, at the price of an escape proof that must be sound and a longer critical section.

### Levels, flags, and build shape

- **Optimization levels**: named bundles of passes and thresholds behind one flag, running from unoptimized builds through size-oriented and speed-oriented sets to a debug-friendly restriction that preserves line and variable mapping, at the price of per-pass control the flag hides and of policy shifts between levels that no source change explains.
- **Phase ordering problem**: passes enable and disable one another, so no single order is best for all programs and a pass pipeline is a maintained judgement rather than a solved one.
- **Iterative compilation**, also **flag autotuning**: recompiles under varied option settings and keeps the best measured result, learned policies replacing hand-tuned heuristics in the same spirit, at the price of a tuning run per program and platform and decisions no one can read.
- **Target feature and tuning selection**: fixes the instruction set a binary requires and the microarchitecture its scheduling, alignment, and idiom choices suit, at the price of a binary that faults on older parts, or of performance tuned to a generation that has passed.
- **Compile time budget**: the bailouts, fixpoint caps, alias query limits, and inlining growth limits that abandon an optimization once its budget is spent, at the price of the largest inputs receiving the least optimization.
- **Optimization remark**: the compiler's report of which transformation applied or failed at a source position, and why, which is how a reader learns what their code is obstructing.

## Working with the machine you have

### Locality and the working set

- **Principle of locality**: the observation that a program at any moment touches only a small part of its address space, in time and in space.
- **Temporal and spatial locality**: the two forms that clustering takes, reuse of one address soon after its last use and use of neighbouring addresses.
- **Working set**: the set of locations a program actively references within a time window, measured against the capacity of a cache level.
- **Reuse distance**, also **stack distance**: the number of distinct locations touched between two successive references to the same location.
- **Miss ratio curve**: a workload's miss rate at every cache capacity, derived in one pass from its reuse distance distribution.
- **Average memory access time**, also **AMAT**: hit time plus miss rate times miss penalty, composed recursively across the levels of the hierarchy.
- **Line utilization**: the fraction of a fetched cache line's bytes read before eviction, the number that condemns a scattered layout.
- **Mechanical sympathy**: writing code shaped to the machine's real cache, alignment, and coherence behaviour, at the price of portability across hardware generations.

### Record and array layout

- **Structure of arrays**, also **SoA**: each field held in its own array so field wise sweeps are contiguous and vectorizable, at the price of scattered whole record access.
- **Array of structures**, also **AoS**: whole records stored one after another so one record is one line fill, at the price of fetching unread fields during field wise sweeps.
- **Array of structures of arrays**, also **AoSoA**: records blocked into vector width groups stored field wise inside each block, at the price of two level index arithmetic.
- **Field reordering**: declaration order permuted so hot fields cluster and padding shrinks, at the price of breaking layout compatibility with external formats.
- **Hot cold field splitting**, also **structure splitting**: frequently used fields separated from rare ones into two allocations, at the price of an extra indirection for cold access.
- **Storage order selection**, also **row major and column major choice**: an array's storage order matched to the loop nest's traversal, at the price of pessimizing another consumer.
- **Array padding**: a dimension enlarged so successive rows stop landing in the same cache sets, at the price of wasted memory and nonstandard strides.
- **Blocked layout**, also **tiled layout**: data stored as submatrix blocks each sized to a cache level, at the price of index arithmetic and awkward partial edge tiles.
- **Morton order**, also **Z order curve**: coordinate bits interleaved so spatial neighbours land near each other in memory, at the price of bit manipulation on every index.
- **Cache conscious search tree layout**, also **Eytzinger layout**, also **van Emde Boas layout**: trees stored implicitly by level or recursively so probes compute addresses, at the price of poor behaviour under insertion.
- **Data oriented design**: a program organized around the layout and bulk transformation of its data, at the price of behaviour scattered away from the state it touches.
- **Entity component layout**, also **archetype storage**: entities grouped by component composition so systems sweep contiguous arrays, at the price of costly composition changes.

### Indirection and inline storage

- **Pointer chasing**: an access pattern in which each address comes from the previous load, serializing memory latency with no overlap.
- **Index instead of pointer**, also **handle based reference**: elements named by array index rather than address, at the price of a base addition and a bounds discipline per dereference.
- **Pointer compression**, also **compressed references**: references stored as narrow offsets from a known base so more fit per line, at the price of a bounded heap.
- **Tagged pointer**: small metadata packed into a pointer's unused bits, at the price of masking on every dereference and assumptions about address width.
- **Offset based reference**, also **relative pointer**: a displacement stored instead of an address so the structure relocates freely, at the price of arithmetic per dereference.
- **Pointer swizzling**: stored identifiers converted into pointers when a structure is loaded, at the price of a fixup pass and images that no longer port.
- **Structure linearization**: a linked structure copied into its traversal order as one contiguous block, at the price of a copy and a layout that goes stale on mutation.
- **Unrolled linked list**: nodes each holding many elements so pointer overhead amortizes, at the price of partly filled nodes and messier insertion.
- **Intrusive container layout**: link fields embedded in the element so no separate node is allocated, at the price of coupling the element to its container.
- **Small buffer optimization**, also **small string optimization**: short contents held inline in the object, at the price of a wider object and a branch on every access.

### Cache lines, alignment, and sharing

- **Cache line**, also **cache block**: the fixed unit of transfer and coherence between levels, sixty four bytes on current mainstream processors.
- **False sharing**: independent variables sharing one line, so a write by one core invalidates the other's data.
- **Cache line padding**: unused bytes inserted so contended fields land on separate lines, at the price of a wasted line per field and fewer objects per line.
- **True sharing contention**: the unavoidable cost when cores genuinely read and write the same variable.
- **Hit modified snoop**, also **HITM**: a load served from another core's modified copy, the counter that identifies genuinely contended sharing.
- **Cache alignment**: an object placed on a boundary of its own size or of a whole line, at the price of padding bytes ahead of it.
- **Read for ownership**: the coherence request that fetches a line and takes exclusive rights before a store may modify it.
- **Full cache line write**: an entire line written at once so no ownership fetch is needed, at the price of requiring aligned and complete writes.
- **Non temporal store**, also **streaming store**: a store routed past the caches for data with no reuse, at the price of severe slowdown if that data is read soon after.
- **Cache line demotion**: a modified line pushed to shared cache so a consumer core need not snoop the producer, at the price of the producer's own reuse.
- **MESI protocol family**, also **MOESI**, also **MESIF**: line states of modified, exclusive, shared, and invalid, extended with owned or forward to name a responder.

### Cache capacity, conflict, and replacement

- **Compulsory, capacity, and conflict miss**: the three reasons a reference misses, a first touch, a working set past capacity, and too many live lines mapping to one set.
- **Cache thrashing**: a pattern in which resident lines evict one another repeatedly so nearly every access misses.
- **Set associativity**: the number of lines one set holds, one in a direct mapped cache and all of them in a fully associative one.
- **Page coloring**: physical frames chosen so a process's pages spread evenly across cache sets, at the price of constraining physical allocation.
- **Cache partitioning**, also **way partitioning**: a shared cache divided so each workload keeps a guaranteed share, at the price of peak utilization and effective associativity.
- **Bélády's optimal replacement**, also **MIN**: evicting the line whose next use is farthest away, the unreachable bound against which real policies are scored.
- **Least recently used replacement**, also **LRU**, also **pseudo LRU**: the entry untouched longest is evicted, at the price of one long non reusing sweep flushing the whole set.
- **Scan resistant segmented policies**, also **SLRU**, also **2Q**, also **LIRS**: entry to a protected segment requires a second reference, at the price of two region sizes to tune.
- **Least frequently used replacement**, also **LFU with aging**: the least referenced entry is evicted and counts decay over time, at the price of choosing a decay schedule.
- **TinyLFU admission**, also **W-TinyLFU**: a frequency sketch decides whether a missed item may enter at all, at the price of sketch memory and stale frequency.

### Blocking, traversal, and prefetch

- **Cache blocking**, also **loop tiling**: a computation restructured so each working block fits a chosen cache level, at the price of extra loop levels and edge cases.
- **Blocking factor tuning**, also **multilevel blocking**: tile sizes chosen separately for registers, first level, and last level cache, at the price of many interacting machine specific parameters.
- **Register blocking**, also **unroll and jam**: a small tile held in registers across iterations, at the price of register pressure and spills.
- **Temporal blocking**, also **time skewing**: tiling across time steps so several sweeps reuse cache resident data, at the price of skewed dependences and halo handling.
- **Loop interchange for locality**: loop levels swapped so the innermost walks memory with unit stride, at the price of legality restrictions from dependences.
- **Loop fusion and fission for locality**: loops merged to reuse values while still cached or split to shrink the working set, at the price of register pressure or an extra traversal.
- **Cache oblivious algorithm**: recursive subdivision that attains near optimal transfers at every level without naming cache parameters, at the price of larger constant factors.
- **TLB blocking**: block sizes chosen so a block's pages fit the translation buffer, at the price of blocks smaller than cache capacity would allow.
- **Hardware prefetcher families**, also **next line**, also **stride**, also **stream**: engines that extrapolate future addresses from observed history and fetch lines before they are demanded.
- **Software prefetch**: an explicit hint issued a tuned distance and degree ahead of use, at the price of instruction slots and pollution when the guess is wrong.
- **Prefetch accuracy and coverage**: the fraction of prefetched lines actually used and of demand misses eliminated, the two numbers that decide whether prefetching pays.

### Translation, paging, and node placement

- **TLB miss**: a translation absent from the buffer, forcing a page table walk whose dependent loads cost more than the access that needed it.
- **TLB reach**: the total span the translation buffer covers, the product of its entry count and the page size.
- **Huge pages**, also **large pages**, also **superpage**: memory mapped in multi megabyte units to extend translation reach, at the price of internal fragmentation and allocation difficulty.
- **Transparent huge pages**: ordinary mappings promoted by the kernel without program changes, at the price of latency spikes from compaction and promotion work.
- **Memory mapped access**, also **mmap**: file data reached through faults on a mapping rather than through copies, at the price of unpredictable fault latency inside ordinary loads.
- **First touch policy**: a page placed on the node of the thread that first writes it, at the price of a layout dictated by initialization code rather than by use.
- **NUMA interleaving**: a region's pages spread round robin across nodes for uniform average bandwidth, at the price of giving up local latency.
- **Memory binding and node affinity**: threads and pages fixed to one node set so each thread touches local memory, at the price of load balancing freedom.
- **Remote access penalty**: the extra latency and reduced bandwidth paid when a core reads memory attached to another node.
- **Page migration**, also **automatic NUMA balancing**: pages moved toward the threads faulting on them, at the price of sampling overhead and migration churn.
- **Memory tiering**: hot data placed in fast memory and cold data in a slower tier, at the price of monitoring overhead and migration latency.

### Bandwidth, DRAM, and the roofline

- **Arithmetic intensity**, also **operational intensity**: the ratio of arithmetic performed to bytes moved from a given level of the hierarchy.
- **Arithmetic intensity improvement**: loaded data reused more before it is discarded, at the price of blocking machinery and register pressure.
- **Memory level parallelism**: the number of independent memory requests a program keeps in flight, bounded by the miss status holding registers.
- **Latency bound versus bandwidth bound**: whether a memory limited loop is held back by dependent access latency or by total transfer rate.
- **Memory bandwidth saturation**: the state in which the memory system delivers its peak rate and further concurrency only raises latency.
- **Cross socket coherence traffic**: the invalidations and transfers that sharing generates over the interconnect, a bounded resource distinct from memory bandwidth.
- **DRAM row buffer locality**: the property that consecutive accesses fall in an already activated row, avoiding a precharge and activation for each one.

### Pipelines and dependence chains

- **Instruction level parallelism**, also **ILP**: the count of mutually independent instructions a single thread offers a superscalar core for simultaneous execution.
- **Latency versus throughput of an instruction**, also **reciprocal throughput**: the distinction between an instruction's result delay and the rate at which independent copies issue.
- **Port pressure**: the demand an instruction mix places on one execution port, which caps throughput while other ports sit idle.
- **Dependency chain**, also **critical path**: the longest sequence of instructions each consuming the previous result, the floor on execution time.
- **Critical dependency chain shortening**: arithmetic restructured so the longest serial chain holds fewer latency cycles, at the price of extra independent instructions and registers.
- **Accumulator splitting**, also **multiple accumulators**: a sum spread over several registers to break one long chain, at the price of registers and a final combining step.
- **Reassociation for parallelism**, also **tree reduction**: an associative operation regrouped into independent subtrees, at the price of changed floating point rounding.
- **Unrolling for instruction level parallelism**: a loop body replicated so independent copies overlap, at the price of code size, a residual tail, and instruction cache pressure.
- **Software pipelining by hand**, also **modulo scheduling**: stages of successive iterations overlapped so one starts every fixed interval, at the price of prologues and register pressure.
- **Instruction footprint reduction**: shorter encodings and smaller hot code so loops fit the instruction and micro operation caches, at the price of losing faster larger sequences.
- **Store forwarding stall**, also **blocked store forwarding**: a load partly overlapping a recent store cannot be forwarded and waits for cache, avoided by matching access widths.

### Branches, dispatch, and speculation

- **Branch misprediction penalty**: the cycles lost refilling the pipeline once a predicted direction or target proves wrong.
- **Branchless programming**: data dependent control flow replaced by arithmetic and masking, at the price of always computing both sides.
- **Conditional move**, also **cmov**, also **select**: a value chosen by predicate without a branch, at the price of a data dependence on the condition.
- **Predication**, also **if conversion**: a small conditional region executed unconditionally with its writes suppressed, at the price of issue slots spent on discarded work.
- **Branch layout for prediction**, also **basic block reordering**, also **hot cold splitting**: hot paths laid out to fall through, at the price of a layout tied to one profile.
- **Test ordering by selectivity**: the cheapest and most discriminating predicate evaluated first, at the price of measuring selectivity in advance.
- **Sorted input branch friendliness**: data presorted so a data dependent branch becomes predictable, at the price of the sort itself.
- **Jump table dispatch**: a branch through an indexed table of targets in constant time, at the price of one hard to predict indirect jump.
- **Threaded dispatch**, also **computed goto**, also **direct threading**: an interpreter jumping straight from one handler to the next, at the price of a duplicated dispatch site per handler.
- **Inline caching**: a call site's resolved target cached for repeat receiver types, at the price of a guard check and collapse once the site turns megamorphic.
- **Guarded devirtualization**, also **speculative devirtualization**: a direct call emitted under a type guard from profile evidence, at the price of the guard and a deoptimization path.
- **Speculation mitigation cost**, also **retpoline**, also **kernel page table isolation**: barriers, predictor flushing, and unmapping that close side channels, at the price of throughput at every domain transition.

### Vector and bit level execution

- **Single instruction multiple data**, also **SIMD**: one instruction applying the same operation to every lane of a packed vector register at once.
- **Automatic vectorization**: the compiler forming vector operations from scalar loops, at the price of fragile recognition defeated by aliasing, early exits, and calls.
- **Vector intrinsics**, also **hand vectorization**: source functions mapping one to one onto vector instructions, at the price of tying the code to one instruction set.
- **Loop tail handling**, also **strip mining**: leftover elements handled by scalar code, masking, or an overlapping final vector, at the price of extra code paths.
- **Masked vector operation**, also **vector predication**: a lane mask applied so inactive lanes stay unmodified, at the price of mask computation and register use.
- **Shuffle and permute**, also **blend**: lanes rearranged or merged under a selector, at the price of pressure on a small number of shuffle ports.
- **Horizontal reduction**: all lanes of a vector collapsed into one scalar, at the price of a serial logarithmic chain outside the main loop.
- **Gather and scatter**: scattered addresses loaded into or stored from one vector, at the price of throughput far below a contiguous access.
- **Fused multiply add**, also **FMA**: a product and a sum computed with one rounding, at the price of results differing from separately rounded arithmetic.
- **Reduced and mixed precision arithmetic**: narrow element types doubling lanes per register while accumulation stays wide, at the price of accuracy, range, and conversion work.
- **Vector unit downclocking**, also **license based frequency reduction**: the core clock drop that dense wide vector use provokes, which can erase the gain it bought.
- **Population count and bit scan**, also **popcount**, also **count leading zeros**, also **count trailing zeros**: single instructions replacing per bit loops over a machine word.

### Threads, tasks, and decomposition

- **Thread pool reuse**: workers kept alive across tasks with a count matched to cores and blocking behaviour, at the price of retained memory and state leaking between tasks.
- **Oversubscription**: more runnable threads than cores, at the price of context switches and cache displacement.
- **Context switch cost**: the register save, scheduler work, and cache and translation refill charged to every switch.
- **Task granularity tuning**, also **sequential cutoff**: task size chosen so scheduling cost stays small against task work, at the price of imbalance once tasks grow coarse.
- **Work stealing**, also **Chase Lev deque**: idle workers taking tasks from the far end of a busy worker's deque, at the price of steal attempts and migration that cools caches.
- **Loop scheduling policy**: iterations assigned statically, dynamically, or in guided shrinking chunks, trading scheduling overhead against imbalance.
- **Domain decomposition**, also **halo exchange**: the problem space split among workers that trade boundary regions each step, at the price of a synchronization point per step.
- **Parallel reduction**, also **scan**: partial results combined in a tree of logarithmic depth, at the price of extra total operations and rounding differences.
- **Barrier synchronization cost**: the time every participant loses waiting for the slowest to arrive, reduced but not removed by tree and dissemination forms.
- **Processor affinity**, also **thread pinning**: a thread fixed to a core so its cache and translation state survive, at the price of the balancer's freedom to migrate it.
- **Simultaneous multithreading**, also **hyperthreading**: several hardware threads sharing one core's execution resources, at the price of per thread slowdown and shared cache pressure.

### Waiting, locks, and contention

- **Lock contention**: the share of time threads spend waiting for a lock rather than executing inside it.
- **Critical section shortening**: work moved out of the locked region, at the price of extra copying or of state visible in an intermediate form.
- **Lock granularity**, also **lock splitting**, also **lock striping**: protected data narrowed or hashed across an array of locks, at the price of whole structure operations and an ordering discipline.
- **Lock ordering**: a global acquisition order fixed to prevent deadlock, at the price of restructuring code that naturally acquires in another order.
- **Reader writer lock**: concurrent readers with exclusive writers, at the price of writer starvation risk and higher uncontended overhead than a plain mutex.
- **Sequence lock**, also **seqlock**: readers retrying against a version counter that writers increment, at the price of readers tolerating torn reads and repeating work.
- **Read copy update**, also **RCU**: a new version published and the old freed only once pre existing readers finish, at the price of deferred reclamation and grace period latency.
- **Spin then block**, also **adaptive spinning**: a short spin with a pause hint before sleeping in the kernel, at the price of a threshold that suits only some wait distributions.
- **Queued spin locks**, also **MCS lock**, also **CLH lock**, also **ticket lock**: waiters queued so each spins on its own line, at the price of a node per waiter and handoff writes.
- **Exponential backoff with jitter**: retry delay multiplied and randomized under contention, at the price of latency added to the eventual success.
- **Hardware lock elision**, also **hardware transactional memory**: a critical section run speculatively without taking the lock, at the price of aborts and a fallback that drags followers onto the slow path.
- **Contention collapse**, also **lock convoy**: total throughput falling as concurrency rises because coordination grows faster than useful work.

### Non blocking building blocks

- **Progress guarantee hierarchy**: the ordering of obstruction freedom, lock freedom, and wait freedom by the strength of progress each promises.
- **Compare and swap loop**: a value read, computed, and published only if it has not changed, at the price of wasted work under contention.
- **ABA problem**: a compare and swap succeeding wrongly because the value changed away and back, defeated by a version tag inside a wider atomic.
- **Treiber stack**: a lock free stack whose push and pop swing the head with one compare and swap, at the price of severe head contention.
- **Michael and Scott queue**: a lock free queue with independent head and tail pointers, at the price of helping logic for a lagging tail.
- **Single producer single consumer ring buffer**: a fixed array with one writer per index so no read modify write is needed, at the price of exactly one thread per end.
- **Marked pointer logical deletion**, also **Harris Michael list**: a node flagged dead in a spare pointer bit before unlinking, at the price of traversals that walk and clean tombstones.
- **Helping mechanism**, also **descriptor based operation**: an operation record published so any thread can finish it, at the price of allocation and indirection per operation.

### Safe memory reclamation

- **Safe memory reclamation**, also **SMR**: the family of protocols that free a node only once no reader can still reach it.
- **Hazard pointers**: each reader publishing the addresses it holds so they are not freed, at the price of a store and a fence per protected access.
- **Epoch based reclamation**: retired nodes freed once every thread has advanced past their epoch, at the price of unbounded memory when one thread stalls inside a section.
- **Quiescent state based reclamation**: memory freed after every thread reports a point where it holds no references, at the price of requiring cooperative reporting.
- **Deferred reclamation**, also **limbo list batching**: retired objects batched and released together, at the price of a higher memory high water mark.
- **Reclamation robustness**: whether one stalled thread can block reclamation forever, the property separating hazard style schemes from epoch style ones.

### Memory ordering and shared state

- **Memory model**: the contract a language or processor gives about permitted reorderings, from total store order to weak models that need explicit barriers.
- **Sequential consistency**: the model in which all threads observe one total order of operations, paid for in fences and store buffer drains.
- **Acquire release semantics**: a load acquire paired with a store release so writes before the release are visible after the acquire, at the price of ordering weaker than a total order.
- **Relaxed atomics**: atomicity without ordering guarantees, at the price of reasoning that is easy to get wrong and bugs that hide on strong hardware.
- **Memory fence**, also **memory barrier**: an instruction forbidding reordering across itself, at the price of pipeline and store buffer serialization, worst for the store load form.
- **Data race**: concurrent unsynchronized access with at least one write, undefined in most models because no happens before edge orders the pair.
- **Publication safety**, also **safe publication**: a fully constructed object made visible only when complete, at the price of a release store or a lock on every publish.
- **Atomic contention collapse**: added threads updating one atomic reducing total progress, since every read modify write serializes on exclusive line ownership.
- **Sharded counter**, also **per CPU counter**, also **striped counter**: increments spread over per thread cells, at the price of a summation on every read and stale totals.
- **Single writer principle**: exactly one thread permitted to write each piece of state, at the price of routing every update through that owner.

### Allocation strategy and avoidance

- **Stack allocation**: storage carved from the call frame and released on return, at the price of lifetimes confined to that frame.
- **Arena allocation**, also **region allocation**, also **bump pointer allocation**, also **memory pool**, also **monotonic buffer resource**: objects served by advancing a cursor through a block freed as a unit, at the price of no individual reclamation.
- **Pool allocation**, also **object pooling**: constructed objects of one size retained and handed out again, at the price of stale state bugs and memory pinned in the pool.
- **Slab allocation**, also **slab coloring**: same type objects carved from page sized slabs offset to spread cache sets, at the price of pages reserved per class.
- **Size class allocation**, also **segregated fit**: requests rounded onto a ladder of block sizes with a free list each, at the price of rounding waste and memory stranded per class.
- **Thread caching allocator design**, also **per thread arenas**, also **magazine layer**: each thread keeping a private block cache so the common path takes no lock, at the price of memory retained per thread.
- **Internal and external fragmentation**: bytes wasted inside rounded up blocks, and free bytes unusable because they are divided too small for pending requests.
- **Allocator blowup**: unbounded footprint growth when freed memory is stranded in per thread caches that never reuse it.
- **Escape analysis driven stack allocation**, also **scalar replacement of aggregates**: objects proved not to escape placed in the frame or in registers, at the price of dependence on fragile analysis.
- **Capacity reservation**, also **amortized doubling**, also **growth factor tuning**: a container's final size reserved or its capacity multiplied on overflow, at the price of slack memory held unused.
- **Zero allocation hot path**: the steady state written to allocate nothing, at the price of preallocated reserves, buffer reuse discipline, and awkward interfaces.

### Garbage collection

- **Tracing collection**, also **mark and sweep**: liveness followed from roots and unmarked blocks returned to free lists, at the price of a full sweep and continued fragmentation.
- **Mark and compact**: marking followed by survivors relocated into a dense block, at the price of copying and updating every reference.
- **Copying collection**, also **scavenging**, also **semispace collection**: survivors copied into fresh space so the old space frees wholesale, at the price of doubled address space.
- **Reference counting collection**: objects freed when their count reaches zero, at the price of update traffic on every assignment and cycles that leak without a tracing backup.
- **Generational collection**: the heap divided by object age so young objects are collected far more often, at the price of write barriers and remembered sets.
- **Region based collection**, also **garbage first**: equal regions collected in sets chosen for reclaimable space and a pause budget, at the price of per region metadata and garbage left behind.
- **Write barrier**, also **card marking**, also **remembered set**: reference stores hooked to record pointers crossing into a collected region, at the price of instructions on every store.
- **Read barrier**, also **load barrier**, also **colored pointers**: loaded references checked and repaired so relocation proceeds concurrently, at the price of work on the far more frequent load path.
- **Concurrent collection**, also **mostly concurrent collection**: collector threads running alongside the application behind short pauses, at the price of barrier overhead, floating garbage, and heap headroom.
- **Nursery sizing and tenuring threshold tuning**: young space size and promotion age chosen so most objects die before promotion, at the price of longer minor pauses and memory.
- **Allocation rate reduction**, also **object lifetime shaping**: fewer bytes allocated per unit of work so cycles come less often, at the price of application code designed around collector behaviour.

### The kernel boundary and the input output path

- **System call overhead**: the mode transition, argument checking, and predictor and pipeline disturbance charged to every entry into the kernel.
- **System call batching**, also **submission batching**: many operations submitted in one entry, at the price of buffering, ring bookkeeping, and delayed error reporting.
- **Asynchronous input output**: operations submitted without blocking and reaped as completions rather than awaited on readiness, at the price of state machines and harder error handling.
- **Buffered input output**: reads and writes staged in user space before crossing to the kernel, at the price of a copy and unflushed data on a crash.
- **Direct input output**: the page cache bypassed so transfers go straight to the device, at the price of strict alignment and of losing kernel caching and readahead.
- **Readahead**, also **sequential access hint**: following blocks fetched before they are requested, at the price of bandwidth and cache spent on data never read.
- **Registered buffers**, also **buffer pinning**: buffers pinned with the kernel once so later operations skip validation, at the price of locked memory held indefinitely.
- **Zero copy transfer**: buffer ownership passed instead of contents copied, at the price of lifetime rules, alignment constraints, and a lost chance to transform the bytes.
- **Kernel bypass**, also **polling mode driver**: a device driven from user space with no kernel entry per operation, at the price of kernel protection, sharing, and a core spent polling.
- **Queue depth tuning**: the number of operations kept in flight fitted to the device, at the price of latency growth once the queue runs too deep.

### Storage layout, indexing, and skipping

- **Columnar storage**, also **column store**: each column's values stored together so a scan reads only what it needs, at the price of expensive row assembly and updates.
- **Lightweight columnar encodings**, also **dictionary encoding**, also **run length encoding**, also **frame of reference**: values coded narrowly per block, at the price of decode work and positional access through an index.
- **Clustering key**, also **sort key**: rows physically ordered by chosen columns so related data sits together, at the price of maintenance writes and re sorting after updates.
- **Multidimensional clustering**, also **z order clustering**: rows interleaved along several dimensions so any of them prunes, at the price of being worse than sorting for one dimension.
- **Zone maps**, also **min max index**, also **block range index**: per block value extremes consulted to skip blocks, at the price of uselessness once values are scattered.
- **Predicate and projection pushdown**: filters and column lists pushed into the scan or the remote source, at the price of duplicated logic and source side capability requirements.
- **Partition pruning**, also **dynamic partition pruning**: partitions that cannot match eliminated at planning or from runtime values, at the price of requiring predicates on the partition key.
- **Covering index**, also **index only scan**: an index carrying every column a query needs, at the price of index size, slower writes, and visibility information near the index.
- **Index selectivity**: the fraction of rows an index predicate admits, the number that decides whether the index beats a scan.
- **Secondary index cost**: the write amplification, space, and maintenance latency every additional index imposes.
- **Membership filter**, also **bloom filter**, also **blocked bloom filter**, also **cuckoo filter**: a compact filter consulted before touching a file, at the price of false positives and bits per key.

### Query execution strategy

- **Vectorized execution**, also **batch at a time execution**: operators running tight loops over column vectors instead of one row per call, at the price of materializing intermediate batches.
- **Whole stage code generation**, also **compiled query execution**, also **operator fusion**: a pipeline fused into one generated loop, at the price of compilation latency and lost operator level observability.
- **Pipeline breaker**: an operator that must consume its whole input before producing output, which bounds where streaming, limits, and adaptation can work.
- **Morsel driven parallelism**: threads pulling small input pieces from a shared queue, at the price of scheduler and shared state complexity.
- **Cardinality estimation**: predicting how many rows an operator produces, the input every cost model and join order depends on.
- **Join algorithm selection**, also **hash join**, also **sort merge join**, also **index nested loop join**: the physical operator chosen from estimated sizes and available orders, at the price of orders of magnitude on a wrong choice.
- **Radix partitioned join**, also **cache sized partitioning**: inputs partitioned by key bits until each fragment fits cache, at the price of extra passes and translation pressure from many output streams.
- **Bloom filter join reduction**, also **runtime filter**, also **semi join reduction**: one side's keys turned into a filter applied to the other side's scan, at the price of construction, a wait, and false positives.
- **Partial aggregation**, also **two phase aggregation**: rows aggregated locally before a shuffle and merged afterwards, at the price of local hash table memory and no gain on unique keys.
- **Spill to disk**, also **external merge sort**: operator state written out once memory is exhausted and merged in later passes, at the price of storage bandwidth and much higher latency.

### The write path and durability

- **Write ahead logging**: changes recorded in a sequential log before the data pages are updated, at the price of writing every change twice.
- **Flush cost**, also **fsync cost**: the latency of forcing buffered data through the device's caches onto stable media.
- **Group commit**, also **epoch based group commit**: several transactions made durable with one flush, at the price of latency for the first transaction in the group.
- **Log checkpointing**, also **fuzzy checkpointing**: dirty pages written and a recovery start point recorded so the log truncates, at the price of write bursts and extra recovery analysis.
- **Write batching**, also **write coalescing**, also **write behind**: small writes accumulated, merged, and acknowledged before reaching stable storage, at the price of a durability window and delayed visibility.
- **Log structured writing**, also **memtable**, also **log structured merge tree**: updates buffered in memory and appended as immutable sorted runs, at the price of stale versions needing later cleanup.
- **Compaction policy**, also **size tiered**, also **leveled**: overlapping runs merged and obsolete versions dropped, at the price of rewriting durable data under a choice between write and space amplification.
- **Write, read, and space amplification**: bytes written, blocks read, and bytes occupied per unit of logical work, the trio no storage engine makes optimal at once.
- **Block and stripe alignment**: request offsets and lengths matched to device blocks and full array stripes, at the price of buffering and padding until a full unit exists.
- **Device level garbage collection**, also **over provisioning**, also **wear leveling**: the device copying valid pages out of blocks it must erase, at the price of hidden capacity and latency spikes.

### Threads and memory on a massively parallel device

- **Single instruction multiple thread execution**, also **SIMT**, also **warp**, also **wavefront**, also **subgroup**: lanes advancing together under one instruction pointer, which makes the group the unit of scheduling, of divergence, and of one memory transaction.
- **Coalesced access**, also **uncoalesced access**, also **memory divergence**: one group's lane addresses arranged to fall in a few contiguous transactions, at the price of index expressions and a record layout the hardware dictates.
- **Grid stride loop**: every thread walking the whole domain in steps of one full grid stride, at the price of a loop per thread and a launch shape sized for the device rather than the problem.
- **Thread coarsening**: one thread given several outputs so loaded values are reused from its own registers, at the price of register pressure and fewer resident threads to hide latency.
- **Warp shuffle exchange**, also **lane exchange**: values passed straight between threads of one group in registers, at the price of a fixed group width and no reach past its boundary.
- **Shared memory carveout**: configurable on chip storage divided between hardware cache and scratchpad, at the price of capacity taken directly from the other consumer for a whole launch.
- **Read only data cache path**: loads annotated read only so they draw on a separate cache, at the price of a promise that nothing writes that memory for the kernel's lifetime.
- **Constant memory broadcast**: a cached read only path serving one address to an entire group in a cycle, at the price of a small fixed budget and serialization when lanes read different addresses.
- **Texture cache locality**, also **texture fetch path**: two dimensional cached fetch with filtering and edge handling in hardware, at the price of a restricted access interface and reduced precision.
- **Local memory spilling**: registers overflowing into slow per thread device memory, the effect that makes an aggressive register budget cost more residency than it bought.

### Getting data onto the device

- **Pinned host memory transfer**, also **page locked buffers**: transfers issued from host buffers the operating system is forbidden to move, at the price of physical memory locked away from every other process.
- **Explicit transfer batching**: many small host to device copies gathered into one large transfer, at the price of a staging buffer and latency for the first item placed in it.
- **Unified memory with explicit prefetch**, also **managed memory**: one address space whose pages migrate on fault, pushed to the device ahead of use, at the price of guessing the access set.
- **Peer to peer device transfer**: device to device copies that never stage through host memory, at the price of code tied to one machine's interconnect topology.

### Explicitly placed memory on a constrained part

- **Scratchpad memory allocation**, also **software managed cache**: objects placed in fast memory with hand written fill and spill rather than left to a cache, at the price of movement code valid for one part.
- **Tightly coupled memory placement**: hot data pinned in single cycle core local memory, at the price of a fixed budget of tens of kilobytes that no later growth may exceed.
- **Cache locking**: critical lines pinned so nothing may evict them, at the price of effective capacity and associativity for every other access the program makes.
- **Code placement in RAM**, also **ramfunc**: hot routines copied out of flash into RAM at boot, at the price of RAM held for a second copy and boot time spent copying.
- **Execute in place**, also **XIP**: code run straight from flash with no copy to RAM, at the price of instruction fetch at flash latency on every miss.
- **Overlay linking**: one memory region reused by several code overlays loaded on demand, at the price of swap time and a partition drawn by hand.
- **Compressed image with boot decompression**: firmware stored compressed and expanded at reset, at the price of boot latency and RAM sized for the expanded image.
- **Static allocation only policy**: heap use forbidden so footprint is provable and fragmentation impossible, at the price of every buffer sized for its worst case at build time.
- **Two level segregated fit allocator**, also **TLSF**: general allocation in bounded time from segregated free lists, at the price of more constant overhead and metadata than a fixed block pool.
- **Stack depth analysis**: worst case stack use bounded statically so no guard is needed at runtime, at the price of forbidding recursion, indirect calls, and variable length arrays.

### Deterministic transfer and real time discipline

- **Direct memory access offload**: bulk transfers handed to a DMA engine so the core keeps running, at the price of cache maintenance around every buffer and setup per transfer.
- **Scatter gather descriptor chaining**: one DMA chain programmed across fragmented buffers, at the price of descriptor memory and a setup cost only long chains repay.
- **Interrupt handler minimization**, also **bottom half**, also **deferred interrupt processing**: the handler acknowledging the device and leaving the work to a schedulable context, at the price of a second scheduling hop and queueing latency.
- **Core isolation for a real time task**: cores reserved with timers and device interrupts routed away from them, at the price of throughput on the reserved cores and imbalance on the rest.
- **Cyclic executive schedule**: a fixed table of work run at fixed offsets in a repeating frame, at the price of slack in every frame and a table rebuilt whenever a task changes.
- **Formatted output elimination**: formatted printing replaced by fixed writers, at the price of losing format strings and of diagnostic code written once per message shape.
- **Worst case execution time analysis**, also **WCET**: a bound on the longest path through a task, derived by static analysis of the code or by measurement on the target.

## Delivering the work to someone

### Deciding before the program runs

- **Compile time evaluation**, also **constexpr**, **consteval**, **comptime**, **compile time function execution**, **macro computation**, **load time value**: computes tables, hashes, and types during translation so runtime reads only results, at the price of a restricted dialect and generated values nobody rechecks.
- **Monomorphization**, also **generic specialization**, **template instantiation**, **type class specialization**, **const generics**, **specialization annotation**: emits a concrete copy of generic code per type so boxing and witness lookup vanish, at the price of binary size and compile time.
- **Partial evaluation**, also **staged compilation**, **multi stage programming**, **supercompilation**, **binding time analysis**: specializes a program on known inputs to produce a residual program, at the price of unpredictable code growth and two level reasoning.
- **Generated code over runtime reflection**, also **source generators**, **annotation processing**, **method handles**, **classmap autoloading**, **view binding**, **compiler macros**: emits accessors and serializers at build time so startup does no introspection, at the price of build machinery and generated sources to review.
- **Ahead of time compilation**, also **native image**, **ready to run**, **closed world compilation**, **install time compilation**, **snapshot build**: compiles the whole program before deployment so no runtime compiler is needed, at the price of reflection needing declaration and no peak speculative optimization.
- **Build action caching**, also **compilation result caching**, **distributed compilation**, **remote build execution**, **hermetic build**, **incremental compilation**, **precompiled headers**, **explicit module build**: reuses build actions keyed by hashed inputs, at the price of strict input declaration and stale state defects.
- **Dead code removal at link**, also **section garbage collection**, **identical code folding**, **assembly trimming**, **symbol visibility hiding**, **resource shrinking**, **icon font tree shaking**: drops what no entry point reaches, at the price of breaking anything resolved by name at runtime and losing function pointer identity.
- **Inlining control**, also **always inline**, **noinline**, **flatten**, **aggressive inlining attribute**, **mid stack inlining**, **method size discipline**: forces or forbids substitution against the compiler's cost model, at the price of instruction cache pressure when the judgement is wrong.
- **Load time binding choice**, also **immediate binding**, **lazy symbol binding**, **prelinking**, **direct binding**, **chained fixups**, **static linking**, **library merging**, **dynamic initializer elimination**: resolves relocations and initializers before first call rather than during it, at the price of slower process start and invalidation when any library changes.

### Keeping values off the heap

- **Escape analysis reliance**, also **stack allocation**, **stackalloc**, **scalar replacement**, **dynamic extent declaration**, **scope allocated instance**, **struct return over pointer return**: keeps values whose pointers never outlive the frame off the heap, at the price of contorting interfaces and a benefit that vanishes when a method grows past the inlining limit.
- **Capacity preallocation**, also **reserve before push**, **map presizing**, **table preallocation**, **preallocated list**, **growth avoidance**: sizes a container once so growth never reallocates, at the price of memory held for an estimate that may be high.
- **Object pooling**, also **array pool rental**, **sync pool reuse**, **node pooling**, **thread local reuse**, **table reuse**, **command pool pooling**: recycles instances instead of allocating fresh ones, at the price of stale state, leaks, and defeating generational collection for cheap objects.
- **Copy on write**, also **clone on write**, **copy on modify**, **uniqueness check**, **copy on write arrays**: shares a buffer between copies until one writes, at the price of a uniqueness check on every mutation and a full copy at the first one.
- **Value type over reference type**, also **struct over class**, **record**, **value class**, **inline class**, **unboxed types**, **transparent representation**, **newtype wrapper**: models data as an identity free type so it needs no allocation or reference counting, at the price of copy cost once it grows and no identity or inheritance.
- **Boxing avoidance**, also **primitive specialization**, **primitive arrays**, **typed arrays**, **specialized arrays**, **array module storage**, **primitive type hints**, **integer cache reliance**: keeps numbers in machine representation rather than wrapper objects, at the price of duplicated declarations per element type and lost generic interfaces.
- **Borrowed views over owned copies**, also **span**, **string view**, **slice parameters**, **memoryview**, **sub binary sharing**, **array views**, **unsafe buffer pointer**: passes a pointer and length instead of constructing a container, at the price of dangling views when the referenced buffer dies first.
- **Zero copy handoff**, also **zero copy deserialization**, **buffer protocol**, **transferable objects**, **shared array buffer**, **out of band buffer serialization**, **shared memory block**, **channel transfer**: shares raw memory across a boundary with no intermediate copy, at the price of lifetime discipline and losing the chance to inspect or transform the bytes.
- **Buffer accumulation over concatenation**, also **string builder**, **iolist**, **table concat**, **string join**, **byte slice writing**, **binary append**: appends into one growable buffer instead of allocating a value per join, at the price of shared mutable state and verbosity at call sites.

### Trading the language's flexibility and safety for speed

- **Devirtualization by closing a type**, also **final**, **sealed**, **private for devirtualization**, **frozen declaration**, **inlinable annotation**, **direct linking**: closes a class or member so calls resolve statically and inline, at the price of foreclosing extension and later redefinition.
- **Closed set dispatch**, also **enum over trait object**, **tagged union visit**, **tag dispatch**, **union splitting**, **dispatch table over conditional chain**, **table driven state machine**: represents a fixed family as a variant type so dispatch is a jump table, at the price of every operation knowing all alternatives.
- **Monomorphic call site discipline**, also **inline cache**, **hidden class stability**, **object shapes**, **profile pollution avoidance**, **first argument indexing**, **implementation pointer caching**: keeps one receiver shape flowing through a hot site so its cache stays single entry, at the price of splitting code that a shared abstraction unified.
- **Dynamic dispatch cost awareness**, also **megamorphic call site**, **witness table dispatch**, **existential container**, **trait object**, **type erasure**, **method cache invalidation**: recognizes that a value reached through an interface carries a table, may allocate, and blocks inlining.
- **Bounds check elimination**, also **inbounds annotation**, **iterator over indexing**, **assertion hints**, **chunks exact iteration**, **split at mut**: shapes code so the compiler proves accesses in range, at the price of a hint that quietly stops working after an edit.
- **Check suppression**, also **pragma Suppress**, **safety zero compilation**, **unchecked indexing**, **runtime safety toggle**, **check pragma push**, **unchecked arithmetic**, **skip locals initialization**, **exclusivity checking disabled**: removes range, index, and overflow checks in a region, at the price of undefined behavior or silent wraparound on any violation.
- **Aliasing promises**, also **restrict qualification**, **noalias pointer**, **argument aliasing prohibition**, **contiguous attribute**, **intent declarations**, **do concurrent**, **vectorization directives**: declares that pointers or arguments do not overlap so values stay in registers and loops vectorize, at the price of undefined results when a caller breaks the promise.
- **Assumption markers**, also **assume attribute**, **unreachable marker**, **likely and unlikely**, **builtin expect**, **pure and const attributes**, **noexcept**, **stability annotation**: states a fact the compiler may take as true without checking, at the price of undefined behavior or termination when it is false.
- **Relaxed floating point**, also **fast math**, **float mode relaxation**, **denormal flushing**, **fixed point arithmetic**: permits reassociation, contraction, and scaled integer substitutes, at the price of reproducibility, range, and correct handling of special values.
- **Runtime feature removal**, also **disabling exceptions**, **disabling runtime type information**, **panic abort**, **no standard library build**, **zero footprint runtime**, **better C mode**, **freestanding build**, **restrictions profile**, **reduced footprint library**: builds without a language facility so its tables and paths vanish, at the price of every library that reports failures or queries types through it.
- **Target specific code generation**, also **march native**, **function multiversioning**, **target feature gating**, **hardware intrinsics**, **portable vector types**, **vector API**: compiles for an exact instruction set or dispatches among compiled variants, at the price of a path per instruction set and binaries that fail on older machines.
- **Type declarations for specialization**, also **type stability**, **concrete field types**, **fixnum arithmetic declaration**, **optimize declaration**, **function barrier**, **global variable avoidance**, **local variable binding**: declares or stabilizes types so the compiler emits specialized machine operations, at the price of restructuring code that changes types conditionally.
- **Interpreter dispatch threading**, also **computed goto dispatch**, **tail call interpreter build**, **Duff's device**, **jump table switch**: threads a bytecode or state loop through an address table so each step jumps directly to the next, at the price of a compiler extension and duplicated dispatch code.

### Laziness, strictness, and fusion

- **Pipeline fusion**, also **stream fusion**, **iterator fusion**, **deforestation**, **foldr build fusion**, **hylomorphism fusion**, **lazy collection view**, **transducer composition**, **sequence pipeline**: merges producer and consumer stages into one loop that builds no intermediate structure, at the price of definitions written in the fusible form and reliance on aggressive inlining.
- **Tail call elimination**, also **tail recursion**, **named let iteration**, **last call optimization**, **tail recursive server loop**, **tailrec annotation**: reuses the caller's frame for a call in tail position so recursion runs in constant stack, at the price of frames absent from stack traces and a restricted recursion shape.
- **Accumulator passing**, also **tail recursion modulo cons**, **difference lists**: carries partial results in an extra parameter so recursion becomes tail recursive, at the price of reversed results and structures usable only once.
- **Strictness analysis**, also **demand analysis**, **absence analysis**, **cardinality analysis**, **boxity analysis**, **occurrence analysis**: infers how much of a value a function needs so thunks, boxes, and unused parameters disappear, at the price of divergence reordered in programs that error.
- **Closure conversion**, also **lambda lifting**, **flat closure conversion**, **defunctionalization**, **continuation passing style**, **uncurrying**, **inline function with reified parameter**: turns nested functions into top level ones over an explicit environment, at the price of environment allocation and longer parameter lists.
- **Thunk control**, also **strictness annotation**, **spine strictness**, **let to case**, **thunk update avoidance**, **blackholing**, **hyperstrictness**: forces a suspension eagerly or skips overwriting it with its result, at the price of losing the laziness that prevented divergence.
- **Case simplification**, also **case of case**, **case of known constructor**, **beta reduction**, **constructor specialization**, **copy propagation of constructors**: pushes analysis into branches and evaluates what is already in view, at the price of duplicated continuation code and code growth.
- **Rewrite rules**: lets a library declare equations the compiler applies as optimizations, at the price of unchecked rules that can change meaning.
- **In place update under a discipline**, also **uniqueness typing**, **linear types**, **transient mutation**, **persistent structure sharing**, **path copying**: proves single ownership so a functional structure may be updated destructively, or rebuilds only the changed path, at the price of a discipline threaded through interfaces or logarithmic access.

### A runtime reaching steady state

- **Warmup driving**, also **just in time warmup handling**, **model warmup requests**, **pipeline warming**, **readiness gating**, **index warmup**, **connection warmup**: runs representative work before serving so hot paths compile and pools fill, at the price of startup time and a harness nobody else needs.
- **Startup snapshot**, also **class data sharing**, **application class data sharing**, **system image building**, **package precompilation**, **frozen modules**, **checkpoint and restore**, **zygote process**: maps a prebuilt heap or class archive so startup skips work already done, at the price of a build step, staleness, and version coupling.
- **Bytecode caching**, also **opcode cache**, **module compile cache**, **code caching**, **preloading**, **timestamp validation disabled**: keeps compiled code across runs and requests so parsing happens once, at the price of stale code until the cache is invalidated.
- **Lazy parsing**, also **eager parse hint**, **eager compilation hints**: leaves function bodies uncompiled until first call, or marks them for immediate compilation, at the price of parsing twice or compiling what never runs.
- **Lazy initialization**, also **initialization on demand holder**, **lazy stored property**, **lazy import**, **lazy require**, **deferred subsystem initialization**, **idle until urgent**: constructs an expensive object at first use rather than at boot, at the price of a stall at the moment of use.
- **Collector selection and heap sizing**, also **collector ergonomics**, **server mode**, **background collection**, **collector target percentage**, **soft memory limit**, **latency mode**, **heap limit raising**: picks a pause and throughput profile and fixes the heap, at the price of memory reserved whether used or not and behavior that shifts with the container's limits.
- **Collector cooperation**, also **thread local allocation buffer**, **compressed object pointers**, **compact object headers**, **string deduplication**, **large object heap awareness**, **heap compaction**, **collector freeze before forking**, **write barrier awareness**: shapes allocation and layout to what the collector rewards, at the price of encoding ceilings, barrier traffic, and objects never reclaimed.
- **Interpreter lock awareness**, also **free threaded build**, **per interpreter isolation**, **multiprocessing over threads**, **cluster process model**, **isolate offload**, **virtual thread offload**: recognizes that one lock serializes bytecode, so parallelism comes from processes, isolates, or a lock free build, at the price of copied arguments, no shared object graph, and higher resident memory.

### Bytes across the network

- **Connection reuse**, also **keep alive**, **persistent connections**, **connection pooling**, **connection coalescing**, **persistent database connections**: reuses an established connection so handshakes are paid once, at the price of sockets and memory held open while idle at both ends.
- **Stream multiplexing**, also **request multiplexing**, **pipelining**: carries many concurrent streams over one connection, at the price of shared congestion control and blocking at the transport layer.
- **Handshake shortening**, also **TLS session resumption**, **zero round trip resumption**, **TCP Fast Open**, **TLS False Start**, **OCSP stapling**, **certificate compression**, **certificate chain trimming**: carries application data or revocation proof inside the handshake, at the price of replay exposure, weaker forward secrecy, and middlebox breakage.
- **Connection racing**, also **Happy Eyeballs**, **anycast routing**, **latency based endpoint routing**: reaches the nearest or first responding endpoint, at the price of duplicate attempts and resets when routes shift mid session.
- **Send policy for small writes**, also **Nagle disabling**, **unsent byte limiting**, **dynamic TLS record sizing**, **packet pacing**, **segmentation offload**: shapes how bytes leave the socket so urgent data is not queued behind bulk data, at the price of more packets, more wakeups, and a later final byte.
- **Congestion window tuning**, also **initial window raising**, **slow start restart disabling**: permits more bytes in flight before the first acknowledgment, at the price of loss when the path cannot absorb the burst.
- **Wire compression**, also **gzip**, **Brotli**, **Zstandard**, **precompressed assets**, **compression level selection**, **payload compression**: encodes bodies before transmission, at the price of processor time at both ends and one of size or speed traded for the other.
- **Delta and dictionary compression**, also **compression dictionary transport**, **delta encoding of responses**, **playlist delta update**: compresses a new version against one the client already holds, at the price of server side version tracking and dictionary distribution.
- **Header compression**, also **HPACK**, **QPACK**: encodes repeated header fields against a shared dynamic table, at the price of per connection state and cross stream dependence.
- **Resource hints**, also **preload**, **prefetch**, **preconnect**, **DNS prefetch**, **early hints**, **module preloading**, **preload scanner discoverability**: tells the client what to resolve, connect to, or fetch before the parser discovers it, at the price of bandwidth on guesses that miss and contention with genuinely critical requests.
- **Priority signalling**, also **fetch priority hinting**, **extensible priorities**, **above the fold prioritization**: reorders the fetch queue by declared importance, at the price of starving resources whose default priority was already right.
- **Head of line blocking avoidance**, also **connection migration**: chooses a transport where one lost packet stalls only its own stream and the connection survives an address change, at the price of loss recovery in user space and path validation work.

### Shipping less code, images, and fonts

- **Bundling**, also **scope hoisting**, **module concatenation**, **bundled server entry point**: concatenates modules into fewer files to cut requests and enable cross module optimization, at the price of coarser cache invalidation and harder stack traces.
- **Code splitting**, also **route based splitting**, **component level splitting**, **granular chunking**, **vendor chunk separation**, **dynamic import**, **deferred library loading**: divides a bundle into chunks fetched on demand, at the price of extra round trips and loading states at the point of use.
- **Tree shaking**, also **side effect free annotation**, **dead code elimination in bundling**, **unused CSS removal**, **barrel file avoidance**: drops exports and rules no entry point reaches, at the price of silent breakage when the side effect claim is false or a name is composed at runtime.
- **Minification**, also **identifier mangling**, **property mangling**, **code shrinking and obfuscation**: rewrites source to the smallest equivalent text, at the price of unreadable traces without a source map and broken reflection on names.
- **Content hashed naming**, also **long term caching**, **immutable asset caching**, **deterministic module identifiers**, **cache busting**: names files by a digest of their contents so they can be cached forever, at the price of a manifest indirection and hash churn when identifiers are unstable.
- **Differential serving**, also **module nomodule pattern**, **transpilation target raising**, **polyfill on demand**, **configuration split delivery**, **application thinning**: ships only the syntax and variants a client can use, at the price of maintaining several outputs and a blocking feature test.
- **Critical path inlining**, also **critical CSS inlining**, **data URI inlining**, **critical data inlining**, **transfer state serialization**: embeds the first view's rules or data directly in the document, at the price of an uncacheable document carrying both markup and the data that produced it.
- **Third party deferral**, also **facade pattern**, **import on interaction**, **deferrable view block**, **on demand feature module**, **on demand resources**, **asset pack delivery**: shows a cheap placeholder and fetches the real thing on first interaction, at the price of a delay right after the click and network dependence at that moment.
- **Delivery budget enforcement**, also **performance budget**, **bundle size analysis**, **instantiation budget discipline**: fails a build when size or timing thresholds are exceeded, at the price of blocked delivery on threshold noise.
- **Image format and variant selection**, also **next generation format delivery**, **responsive images**, **srcset and sizes**, **art direction**, **client hints**, **breakpoint generation**: offers encodings and widths so the client takes one that fits its layout and support, at the price of many derivatives, negotiation logic, and cache dilution across variants.
- **Perceptual image encoding**, also **perceptual quality targeting**, **quantization table tuning**, **lossless recompression**, **chroma subsampling**, **metadata stripping**: compresses each asset only until a perceptual threshold is met, at the price of an encoding search per asset and bleeding on saturated edges and text.
- **Placeholder reveal**, also **progressive JPEG**, **interlacing**, **blur up**, **low quality image placeholder**, **dominant color placeholder**, **dimension attributes**, **aspect ratio reservation**: reserves the box and shows something coarse before the detail arrives, at the price of extra inline bytes and a visible pop on load.
- **Lazy image loading with an eager hero**, also **loading lazy**, **decoding async**, **asset inlining of sprites**, **sprite sheets**: defers offscreen images, exempts the largest visible one, and packs small ones into a single addressed file, at the price of blank frames during fast scrolling and invalidating a sheet when one member changes.
- **Font subsetting**, also **unicode range subsetting**, **incremental font transfer**, **WOFF2 compression**, **vector path simplification**: ships only the glyphs a page needs, at the price of missing characters in user supplied text and many small requests on mixed script pages.
- **Font display strategy**, also **font-display**, **metric override**, **two stage font loading**, **system font stack**, **font preloading**: chooses whether text blocks, swaps, or paints in a reshaped fallback while a face loads, at the price of either invisible text or a reflow.

### Caching between the origin and the client

- **Edge caching**, also **content delivery network**, **tiered caching**, **origin shield**, **regional shield cache**, **image transformation at the edge**: holds copies near users with one upstream cache facing the origin, at the price of invalidation lag and concentrated load on the shield.
- **Cache key normalization**, also **vary header discipline**, **vary aware caching**: canonicalizes keys so equivalent requests share one entry, at the price of wrong hits when a dropped parameter mattered and hit rate fragmentation when it did not.
- **Stale while revalidate**, also **stale if error**, **soft purge**: serves a stale entry immediately while refreshing behind it, or when the origin fails, at the price of users seeing old data and outages hidden from monitoring.
- **Request collapsing**, also **request coalescing**, **cache stampede prevention**, **probabilistic early expiration**, **refresh ahead**: merges concurrent misses for one key into a single origin fetch, at the price of every waiter sharing one failure.
- **Tag based invalidation**, also **surrogate key purge**, **key namespace versioning**, **on demand revalidation**, **event driven invalidation**: retires groups of entries by label rather than by URL, at the price of bookkeeping at write time and orphaned memory until eviction.
- **Conditional revalidation**, also **entity tag validation**, **last modified validation**, **heuristic freshness**, **max age tuning**, **time to live tuning**: asks for a resource only if it changed since a known version, at the price of a round trip even on a hit and unpredictable staleness where no lifetime is declared.
- **Cache write policy**, also **cache aside**, **read through**, **write through**, **write behind**, **negative caching**: decides who loads a missing entry and when the store is written, at the price of a slow first request per key, added write latency, or loss on failure.
- **Service worker caching**, also **cache first**, **network first**, **offline first**, **precaching**, **runtime caching**, **navigation preload**, **background sync**: answers requests from a client side proxy store, at the price of an update lifecycle that can pin old code and unbounded growth without eviction.
- **Rendered output caching**, also **full page output caching**, **fragment caching**, **edge side includes**, **incremental static regeneration**, **application shell pattern**: stores rendered pages or fragments keyed by their inputs, at the price of invalidation across every input that shaped the output.
- **Compute at the edge**, also **edge rendering**, **edge computing placement**, **compute at points of presence**: runs request logic in the cache tier instead of the origin, at the price of a constrained runtime, a split codebase, and distant data access.
- **Instant history navigation**, also **back forward cache**, **paint holding**: keeps a page snapshot resident or the old page painted until the next has content, at the price of eligibility rules that forbid common patterns and delayed acknowledgment of the navigation.
- **Cache hit ratio**, also **cache partitioning cost**: the share of requests a cache satisfies rather than forwarding, and the reuse lost when browsers key caches by top level site.

### Where markup is built and when it wakes

- **Server side rendering**, also **isomorphic rendering**, **universal rendering**: produces markup on the server for the first response, at the price of server compute, a later first byte, and code restricted to what both runtimes support.
- **Static site generation**, also **incremental static regeneration**, **on demand revalidation**: renders pages at build time and rebuilds them in the background after a lifetime, at the price of full rebuilds and the first viewer after expiry seeing old output.
- **Client side rendering**: ships a near empty document and builds the interface in the browser, at the price of a blank first paint and content that exists only if script runs.
- **Streaming server rendering**, also **out of order streaming**, **early flush**, **shell first response**, **streaming placeholders**: flushes markup as it is produced and fills slow regions when their data resolves, at the price of no late headers or status and layout shift as regions fill.
- **Partial hydration**, also **progressive hydration**, **selective hydration**, **lazy hydration on visibility**, **hydration on interaction**, **islands architecture**: attaches behavior only to the parts that need it, in the order interaction demands, at the price of boundary discipline and regions that do not respond for their first moments.
- **Resumability**, also **event replay hydration**, **server components**, **zero JavaScript baseline**: serializes framework state into the document and replays interactions that arrived early, so the client never repeats setup, at the price of larger markup and a specialized runtime.
- **Progressive enhancement**, also **HTML over the wire**, **fragment swapping**: delivers a working document and layers script behavior over it, returning rendered markup for updates, at the price of designing every feature at two capability levels and tighter server coupling.
- **Hydration mismatch**, also **double data problem**: the defect class where client render output disagrees with server markup, forcing a discard, and the waste when a page carries both markup and the data behind it.
- **Render as you fetch**, also **route level data loaders**, **preemptive data fetching**, **parallel data fetching**, **request batching**, **persisted queries**, **normalized client cache**: starts code and data requests at navigation instead of at component mount, at the price of routing that must declare data needs and load spikes that are hard to attribute.
- **Request waterfall**, also **fetch on render**: the dependency chain in which each request cannot start until a previous one returns, produced when every component fetches on mount.
- **Speculative navigation**, also **prefetch on intent**, **viewport entry prefetch**, **idle time prefetching**, **speculation rules**, **prerendering**, **signed exchange prefetch**, **connection aware gating**: starts a navigation's work once a click becomes probable, at the price of duplicate work, origin side effects, and bytes spent on wrong guesses.

### Client update work, layout, and the main thread

- **Tree diffing**, also **virtual DOM diffing**, **keyed reconciliation**, **key stability**, **track by function**, **diffable data source updates**: compares a cheap description of the tree against the last one and applies only differences, at the price of allocating and walking that description on every render.
- **Compile time reactivity**, also **patch flags**, **static subtree hoisting**, **const widget subtree**, **single render directive**, **constant constructor canonicalization**: annotates at build time which bindings can change so the runtime skips the rest, at the price of a template language the compiler controls.
- **Fine grained reactivity**, also **signals**, **external store subscription**, **shallow reactivity**, **deferred state read**, **dirty checking**: subscribes individual bindings to the values they read instead of rescanning watched expressions, at the price of dependency bookkeeping and manual tearing protection.
- **Render bailout**, also **component memoization**, **pure component checks**, **push based change detection**, **detached change detector**, **skippable composable**, **equatable view conformance**, **pure pipe**: skips a subtree whose observed inputs compare equal, at the price of comparison work and stale output when the comparison lies.
- **Referential stability**, also **callback memoization**, **selector memoization**, **structural sharing**, **derived state caching**, **context splitting**, **view identity stability**: keeps object and function identities constant between renders so equality checks succeed, at the price of caches held for their lifetime and closures over old values.
- **Concurrent rendering**, also **batched updates**, **transition marking**, **time slicing**, **deferred value**, **offscreen rendering**: prepares a render off screen at declared urgency and yields between slices, at the price of components tolerating repeated work and results shown for stale input.
- **List virtualization**, also **windowing**, **overscan**, **variable height estimation**, **content visibility**, **contain intrinsic size**, **below the fold deferral**: renders only the rows inside the viewport behind a sized spacer, at the price of broken find in page and scrollbar jitter as estimates resolve.
- **View recycling**, also **DOM recycling**, **view holder pattern**, **cell reuse**, **lazy view inflation**, **prefetching data source**, **uncontrolled inputs**: reuses scrolled out views and lets the platform own field state, at the price of resetting every field on bind and stale state leaking between items.
- **Read write batching of layout**, also **layout thrashing avoidance**, **forced synchronous layout avoidance**, **measurement caching**, **detached DOM mutation**, **document fragment batching**: groups all measurements before all mutations and edits subtrees outside the document, at the price of an explicit scheduling layer, stale measurements, and lost focus and scroll position.
- **Containment**, also **layout containment**, **paint containment**, **style containment**, **style scoping**, **expensive selector avoidance**, **DOM size reduction**, **layout hierarchy flattening**: promises the engine that a subtree's effects stay inside it and keeps matching shallow, at the price of losing sizing and overflow interaction with the outside and duplicating rules across scopes.
- **Compositor only animation**, also **transform and opacity animation**, **layer promotion**, **will change hints**, **layer rasterization caching**, **opaque layer marking**, **composited scrolling**, **off main thread animation**: animates and scrolls what the compositor can handle without layout or paint, at the price of video memory, layer explosion, and no per frame script control.
- **Paint work reduction**, also **paint area reduction**, **overdraw reduction**, **offscreen pass avoidance**, **shadow path precomputation**, **corner mask replacement**, **tiled rasterization on a dedicated thread**, **layout shift avoidance**: shrinks the invalidated region and the number of times a pixel is written, at the price of flatter visual design and checkerboarding when raster falls behind.
- **Main thread yielding**, also **long task splitting**, **cooperative scheduling**, **input pending check**, **priority based task scheduling**, **animation frame scheduling**, **idle callback deferral**, **request cancellation**: returns control to the event loop so queued input is handled, at the price of longer total completion and low value work that may never run.
- **Event rate reduction**, also **debouncing**, **throttling**, **pointer event coalescing**, **event delegation**, **passive event listeners**, **event queue batching**: collapses a burst of events into one handler run per interval or frame, and attaches one listener high in the tree, at the price of added latency, lost intermediate positions, and manual target resolution.
- **Thread offload**, also **web worker**, **worker pool**, **isolate offload**, **offscreen canvas**, **WebAssembly offload**, **vector instruction offload**, **graphics compute offload**, **structured clone cost**: moves computation off the thread that paints, at the price of message passing, duplicated state, and a boundary crossing for every value.

### Perceived speed, device limits, and the metrics

- **Perceived performance**: the speed a user experiences, determined by feedback and ordering rather than by total elapsed work.
- **Response time thresholds**, also **Doherty threshold**, **response time limits**, **progress indication thresholds**, **spinner delay threshold**, **minimum indicator duration**: the intervals deciding whether a wait deserves no indicator, a spinner, or a determinate bar.
- **Structural waiting states**, also **skeleton screens**, **shimmer placeholder**, **staged reveal**, **transition masking**, **perceptual ordering**: shows the shape of the eventual layout and fills it in the order the user is looking, at the price of a second representation of every view and fixed delay added to responses that were already fast.
- **Instant acknowledgment**, also **local echo**, **optimistic user interface updates**, **input latency reduction**, **first input delay reduction**: paints a response inside the first frame and applies the expected result before the server confirms, at the price of rollback logic and visible reversals on failure.
- **Client side prediction**, also **rollback reconciliation**, **lag compensation**, **dead reckoning**, **entity interpolation**, **input buffering**: simulates the outcome locally while the authoritative result travels, at the price of correction artifacts, stored history, and deliberately added display latency.
- **Adaptive loading**, also **effective connection type gating**, **Save-Data awareness**, **device memory tiering**, **core count tiering**, **low end device tier detection**, **model variant selection by tier**: varies payload, quality, and features by the device and network actually present, at the price of many code paths to test and coarse, spoofable signals.
- **Sustained performance limits**, also **thermal throttling**, **sustained performance mode**, **battery aware degradation**, **frame rate capping**, **power capping**, **race to idle**, **duty cycling**, **tickless idle**: the clock a device can hold indefinitely, and the choices that trade peak throughput and latency to stay inside it.
- **Deferrable work scheduling**, also **background fetch**, **inexact alarm batching**, **radio tail awareness**, **sleep bucket compliance**, **wake lock avoidance**, **offscreen work suspension**: batches background work under platform constraints such as charging, network, and idle state, at the price of unpredictable timing and resumption latency.
- **Core Web Vitals**, also **Largest Contentful Paint**, **Interaction to Next Paint**, **Cumulative Layout Shift**: the load, interactivity, and stability metrics published as the shared field baseline for a delivered page.
- **Load timeline metrics**, also **Time to First Byte**, **First Contentful Paint**, **Speed Index**, **Total Blocking Time**, **Time to Interactive**, **long task**, **time to initial and full display**, **pre main and post main launch time**, **cold, warm, and hot start**: the named instants and sums that decompose one load into attributable parts.
- **Metric attribution**, also **Largest Contentful Paint subparts**, **Interaction to Next Paint subparts**, **Long Animation Frames**, **Element Timing**, **Event Timing**, **Layout Instability**, **Navigation and Resource Timing**, **Server Timing**, **user timing marks**, **frame metrics reporting**: reports that split a metric into the phases, scripts, and nodes responsible for it.
- **Field data against lab data**, also **real user monitoring**, **synthetic monitoring**, **percentile thresholding**, **critical request chain**: the distinction between measurements from real sessions and controlled runs, judged at a high percentile so tail experience governs.
- **Frame budget**, also **frame time**, **jank**, **dropped frame**, **one percent low frame rate**, **jank rate**, **motion to photon latency**, **RAIL model**, **buffer underrun**: the wall clock allowance one frame has, and the measures of missing it.

### Choosing what to draw and at what detail

- **Cheap rejection tests**, also **frustum culling**, **scene graph hierarchy culling**, **visibility layer masks**, **scissor restriction**, **distance culling**, **detail culling**, **contribution culling**, **small triangle culling**, **backface culling**, **cluster cone of normals**, **audible radius culling**: rejects whatever falls outside the view, faces away, or contributes negligibly, at the price of a test per object and pop in or flicker at the threshold.
- **Occlusion culling**, also **hierarchical z buffering**, **occlusion queries**, **two pass culling**, **depth reprojection culling**, **software occlusion rasterization**, **predicated rendering**, **potentially visible set**, **portal culling**, **occluder proxy geometry**: rejects objects hidden behind nearer geometry, at the price of visibility work that can exceed the cost of drawing them and a frame of latency reading results back.
- **Depth ordering**, also **depth prepass**, **early depth test**, **front to back sorting**, **depth bounds test**, **stencil masking**, **transparency sorting**, **alpha test against alpha blend**: fills depth cheaply and draws opaque geometry nearest first so later fragments never shade, at the price of submitting geometry twice and rejection defeated by discard or blending.
- **Spatial acceleration structures**, also **bounding volume hierarchy**, **axis aligned box and sphere tests**, **octree**, **quadtree**, **k-d tree**, **binary space partitioning**, **uniform grid**, **spatial hashing**, **surface area heuristic**, **refitting**, **Morton order sorting**, **sweep and prune**, **broad phase pruning**, **screen space binning**: organizes space so one query rejects whole subtrees or reaches only nearby candidates, at the price of build time and quality degrading as contents move.
- **Level of detail**, also **discrete**, **continuous**, **view dependent**, and **hierarchical level of detail**, **progressive meshes**, **geomorphing**, **dithered transition**, **level of detail popping**: substitutes a cheaper representation as an object's screen contribution falls, and blends across the switch, at the price of authoring several versions and drawing both during the overlap.
- **Mesh simplification and proxies**, also **decimation**, **edge collapse**, **quadric error metric**, **impostors**, **billboards**, **octahedral impostors**, **billboard clouds**, **detail baking**, **shadow proxy geometry**, **collision proxy simplification**: approximates a surface with fewer triangles, a rendered image, or a primitive shape, at the price of silhouette loss, parallax error, and imprecise contacts.
- **Terrain and virtualized geometry**, also **chunked terrain level of detail**, **geometry clipmaps**, **adaptive tessellation**, **meshlet clustering**, **virtualized geometry**, **ray traced geometry level of detail**: streams and refines a surface so detail matches pixels rather than authored levels, at the price of seams, stitching, and a rigid asset pipeline.
- **System level of detail**, also **animation level of detail**, **simulation level of detail**, **audio level of detail**, **decoupled update rates**, **sleeping bodies**, **update budgeting**, **dirty flag updates**: coarsens a system's update rate or solver quality with distance and importance, at the price of visible stepping and discontinuity when an entity matters again.

### Submitting the frame's work

- **Draw call batching**, also **static batching**, **dynamic batching**, **mesh merging**, **instancing**, **texture atlasing**, **texture array binding**: merges objects that share state into fewer submissions, at the price of losing independent culling and per object updates.
- **Device driven submission**, also **indirect drawing**, **multi draw indirect**, **GPU driven rendering**, **mesh shaders**, **work graphs**, **programmable vertex fetch**: reads draw parameters from device memory so the device decides what to draw, at the price of a complex pipeline, lost fetch hardware, and no host visibility for debugging.
- **State sorting**, also **material sorting**, **state change minimization**, **descriptor set reuse**, **bindless resources**, **descriptor indexing**, **push constants**, **uniform buffer packing**: orders draws so pipeline and resource bindings change as rarely as possible, at the price of losing depth ordering benefits and static validation of bindings.
- **Command reuse**, also **command buffer reuse**, **render bundles**, **secondary command buffers**, **multithreaded command recording**, **render graph scheduling**, **frame graph**: records a sequence once and replays it, or declares passes and lets the engine order, alias, and prune them, at the price of invalidation whenever anything referenced changes and an abstraction layer over the pipeline.
- **Pipeline precompilation**, also **shader precompilation**, **pipeline state object caching**, **pipeline cache serialization**, **pipeline warming**, **specialization constants**, **permutation reduction**, **uber shader tradeoff**, **pipeline library linking**: compiles every variant before first use, at the price of load time, disk for compiled variants, or runtime branching and unused work per pixel.
- **Suballocation and upload**, also **memory suballocation**, **ring buffer allocation**, **persistently mapped buffers**, **staging buffer upload**, **host visible device writes**, **upload budgeting**, **render target aliasing**, **memory compaction**: carves per frame data and targets out of a few large device allocations, at the price of writing an allocator, manual synchronization, and a hard per frame ceiling.
- **Barrier and queue discipline**, also **resource barrier minimization**, **split barriers**, **timeline semaphore synchronization**, **fence based synchronization**, **asynchronous transfer queue**, **multi queue submission**, **asynchronous compute**, **readback avoidance**: batches transitions and overlaps queues instead of coarse device idles, at the price of subtle hazards, cross queue synchronization, and decisions delayed a frame.
- **Residency and streaming**, also **mipmapping**, **block compression**, **transcodable texture format**, **texture streaming**, **virtual texturing**, **sparse textures**, **texture pool budget**, **least recently used eviction**, **level streaming**, **proximity prefetching**, **pack file layout ordering**, **vertex attribute quantization**, **mesh compression**, **loading screen hiding of work**: keeps only the pages and mip levels the current view needs and fetches the rest as the viewer approaches, at the price of visible blur and pop in when the stream falls behind, and thrashing when the working set exceeds capacity.

### Shading, temporal reuse, and frame delivery

- **Deferred shading**, also **visibility buffer rendering**, **deferred texturing**, **G buffer packing**, **deferred decals**: writes surface attributes to buffers and lights once per pixel afterwards, at the price of bandwidth, an indirection to resolve material data, and awkward transparency.
- **Light culling by tile**, also **forward plus**, **tiled light culling**, **clustered light culling**, **light linked list**, **stencil light volume masking**, **light budget capping**: assigns lights to screen tiles or depth clusters so each pixel loops only over nearby ones, at the price of a binning pass and lights silently dropping out.
- **Baked and probe lighting**, also **light maps**, **precomputed radiance transfer**, **light probes**, **irradiance volumes**, **spherical harmonic irradiance**, **dynamic diffuse global illumination**, **irradiance and radiance caching**, **radiance cascades**, **surfel based lighting**, **screen space radiance probes**, **baked acoustic parameters**: precomputes or caches incoming light at points and interpolates it, at the price of immutable geometry, probe placement, and leaking across thin occluders.
- **Traced illumination**, also **voxel cone tracing**, **signed distance field tracing**, **hybrid rendering**, **ray budget**, **next event estimation**, **multiple importance sampling**, **resampled importance sampling**, **ReSTIR**, **light tree sampling**, **Russian roulette termination**, **blue noise distribution**, **wavefront path tracing**, **ray sorting**, **shader execution reordering**, **firefly clamping**: traces cones, fields, or a fixed budget of rays where rasterization cannot answer, at the price of two pipelines, noise, bias, and correlation artifacts.
- **Reconstruction from sparse samples**, also **ray traced denoising**, **spatiotemporal variance guided filtering**, **depth aware upsampling**, **half resolution effects**, **screen space ambient occlusion**: rebuilds a clean image from few noisy samples using spatial and temporal filtering, at the price of ghosting, halos, and lost fine detail.
- **Shader cost reduction**, also **occupancy tuning**, **register pressure reduction**, **texture fetch reduction**, **lookup texture precomputation**, **analytic approximation**, **precision qualifier lowering**, **shader level of detail**, **material quality tiers**, **early out in shaders**, **wave divergence reduction**: shortens the work one invocation performs, at the price of recomputed values, interpolation error, banding, and visible material discontinuities.
- **Shadow map management**, also **shadow map cascades**, **sample distribution shadow maps**, **shadow atlas**, **shadow caching**, **virtual shadow maps**, **cascade update staggering**, **screen space contact shadows**, **texture space shading**: splits the range into maps of decreasing density and refreshes only what moved, at the price of a pass per cascade, seams at splits, and lag in distant shadows.
- **Temporal reuse**, also **temporal antialiasing**, **temporal reprojection**, **history buffer**, **sample jittering**, **motion vector reuse**, **amortized rendering**, **interleaved rendering**, **temporal and spatial upsampling**, **checkerboard rendering**, **variable rate shading**, **dynamic resolution scaling**, **foveated rendering**, **frame generation**: renders fewer pixels or samples per frame and reconstructs the rest from history, at the price of blur, ghosting, holes at disocclusions, and artifacts on thin moving detail.
- **Frame delivery**, also **frame pacing**, **double and triple buffering**, **vertical synchronization**, **adaptive synchronization**, **render queue depth limiting**, **latency reduction modes**, **late input sampling**, **late latching**, **predicted pose**, **asynchronous time warp**, **flip model presentation**, **fixed timestep with interpolation**, **job system scheduling**, **render thread decoupling**, **tile memory load and store actions**: regulates when frames are presented, how far the host runs ahead, and how late input may be read, at the price of holding back ready frames, one frame of added latency, and reprojection artifacts when a deadline is missed.

### Encoded media, video and audio

- **Rate control mode**, also **constant rate factor**, **capped constant rate factor**, **two pass rate control**, **constant bitrate**, **variable bitrate audio**, **decoder buffer model compliance**: targets a quality level or a fixed output rate, at the price of unpredictable file size, or quality collapse in complex scenes.
- **Reference structure tuning**, also **group of pictures structure**, **hierarchical bidirectional frames**, **reference frame count**, **intra refresh**, **scene cut detection**, **lookahead window sizing**, **segment duration tuning**: sets keyframe spacing and prediction depth, at the price of random access traded against bitrate, plus latency and buffered memory.
- **Perceptual mode decision**, also **rate distortion optimization**, **trellis quantization**, **adaptive quantization**, **macroblock tree bit allocation**, **psychovisual tuning**, **motion search pattern**, **subpixel refinement**, **encoder preset**, **psychoacoustic masking model**, **bit reservoir**, **joint stereo coding**, **spectral band replication**, **parametric stereo**: spends bits only where the eye or ear detects error, at the price of large encoder time and imaging or synthetic detail where parameters replace signal.
- **Encoder and decoder offload**, also **slice based parallel encoding**, **tile based coding**, **wavefront parallel processing**, **frame level parallelism**, **hardware encoder offload**, **hardware decode offload**, **zero copy decode to texture**, **transmuxing**, **film grain synthesis**: divides a frame into independent units or hands coding to a fixed function block, at the price of compression efficiency at boundaries and lost tuning control.
- **Per title ladder construction**, also **per shot encoding**, **convex hull ladder**, **metric targeted encoding**, **just noticeable difference spacing**: derives resolution and rate rungs from each asset's own complexity, at the price of many analysis encodes.
- **Adaptive bitrate streaming**, also **media segmentation**, **CMAF**, **low latency HLS and DASH**, **chunked segment delivery**, **byte range addressing**, **just in time packaging**, **live edge manifest caching**, **trick play track**, **thumbnail sprite track**: cuts a stream into cacheable segments among which a player switches, at the price of per segment request overhead, visible quality shifts, and origin load.
- **Rate adaptation and layering**, also **throughput based adaptation**, **buffer based adaptation**, **startup rendition selection**, **segment prefetching**, **content steering**, **scalable coding layers**, **temporal layer dropping**, **simulcast**, **selective forwarding**: chooses or forwards a rendition from measured bandwidth, buffer occupancy, or an available layer, at the price of oscillation on noisy links and encode and uplink cost for every layer.
- **Real time media repair**, also **jitter buffer sizing**, **packet loss concealment**, **forward error correction**, **retransmission on negative acknowledgment**, **redundant audio encoding**, **keyframe request**, **delay based bandwidth estimation**, **transport wide congestion feedback**, **send side pacing**, **discontinuous transmission**, **comfort noise generation**: absorbs arrival variance and repairs loss without waiting for a full round trip, at the price of added latency, bandwidth spent on healthy paths, and audible artifacts.
- **Real time audio discipline**, also **callback buffer sizing**, **block based processing**, **lock free ring buffer handoff**, **denormal flushing**, **voice limiting**, **virtual voices**, **voice stealing**, **submix bus consolidation**, **sample residency choice**, **partitioned convolution**, **overlap add and overlap save**, **polyphase resampling**, **downmixing**, **ambisonic order reduction**, **binaural filter approximation**: forbids allocation, locks, and file access inside the audio callback, processes in blocks, and caps concurrent voices, at the price of complex handoff to worker threads, one block of latency, and audible dropouts at the cap.

### Placing work across machines

- **Horizontal against vertical scaling**, also **scale out**, **scale up**, **elasticity**: adds machines so aggregate throughput rises with count, or moves the workload onto a larger machine, at the price of coordination and state partitioning against a hard ceiling and coarse cost steps.
- **Autoscaling**, also **reactive**, **predictive**, **scheduled**, **target tracking**, and **step scaling**, **cluster autoscaling**, **event driven autoscaling**, **custom metric autoscaling**, **vertical workload autoscaling**, **right sizing**, **requests and limits tuning**: adjusts capacity from load signals or a forecast, at the price of reaction lag, thrash, restarts, and degraded latency during the ramp.
- **Capacity headroom and commitments**, also **over provisioning**, **utilization target tuning**, **burstable capacity**, **reserved commitment**, **spot capacity**, **preemptible capacity**, **spot pool diversification**, **interruption handling with checkpoints**, **non production scheduling**, **idle resource reclamation**: runs deliberately below capacity, or on discounted interruptible capacity, at the price of paid idle resources, severe throttling once credit is spent, and reclamation handling.
- **Scale to zero and cold start mitigation**, also **warm pool**, **provisioned concurrency**, **keep warm pinging**, **snapshot restore startup**, **container image size reduction**, **lazy image pulling**, **layer caching**, **dependency trimming**, **initialization outside the handler**, **connection reuse across invocations**, **micro virtual machine isolation**, **placeholder overprovisioning**: releases capacity while idle and shortens the initialization of a fresh environment, at the price of a cold start on the next request or paying for capacity that serves nothing.
- **Bin packing against spread placement**, also **affinity**, **anti affinity**, **gang scheduling**, **topology aware scheduling**, **rack awareness**, **zone aware routing**, **node consolidation**, **descheduler rebalancing**, **resource overcommit**, **multi tenancy density**, **priority and preemption classes**: packs tasks onto the fewest machines, or spreads them across failure domains, at the price of contention between neighbors on one side and lower density and longer paths on the other.
- **Isolation partitions**, also **cell based architecture**, **shuffle sharding**, **bulkhead isolation**, **resource quota**, **quality of service classes**, **workload class separation**, **static stability**, **tenant level rate isolation**, **sidecar overhead**, **node level data plane**: gives each cell, tenant, or dependency its own resources so saturation cannot spread, at the price of duplicated infrastructure and stranded capacity.
- **Sharding and key routing**, also **horizontal and vertical partitioning**, **consistent hashing**, **virtual nodes**, **rendezvous hashing**, **bounded loads**, **Maglev hashing**, **session affinity**, **deterministic subsetting**, **round robin**, **least connections**, **power of two choices**, **outlier detection ejection**, **slow start ramping**, **direct server return**, **service discovery caching**: assigns each key or request to one backend, at the price of cross shard queries, rebalancing, imbalance from hot keys, and decisions made on stale state.
- **Locality of data and spend**, also **moving computation to the data**, **co partitioning**, **reference data replication**, **follow the workload**, **follow the sun scheduling**, **geographic partitioning**, **edge computing placement**, **cross zone traffic avoidance**, **egress reduction**, **carbon aware scheduling**, **cost allocation tagging**, **unit economics tracking**, **storage class transition**: runs work where its input already sits and inside the cheapest boundary, at the price of scheduling constraints, cluster imbalance, and cross region operations for mobile users.

### Holding down the tail

- **Tail at scale mitigation**, also **tail latency amplification**, **fan out reduction**, **canary request**: the family of techniques holding high percentiles down when one request touches many servers, and the amplification that forces them.
- **Request hedging**, also **tied requests**, **backup requests**, **hedged read**, **hedging budget**, **selective replication of hot items**, **hot key request replication**: sends a duplicate after a delay and takes the first reply, at the price of extra load on every hedged path and consistency work for the extra copies.
- **Straggler mitigation**, also **speculative execution**, **speculative task duplication**, **micro partitioning for balance**, **latency induced probation**, **work stealing across nodes**, **shared work queue dispatch**: relaunches or reroutes the slowest participants and takes the first finisher, at the price of wasted capacity and lost locality.
- **Deadline propagation**, also **timeout budget splitting**, **cancellation propagation**, **server side queue timeout**, **earliest deadline first ordering**, **long request time slicing**: passes the remaining time budget down the chain so doomed work stops early, at the price of protocol plumbing, clock discipline, and cancelling slow but recoverable steps.
- **Degraded answers**, also **scatter gather with partial results**, **good enough response**, **brownout**, **graceful degradation**, **adaptive model downgrade under load**: answers from a cheaper path or with whatever arrived before the deadline, at the price of result quality and completeness.
- **Admission control**, also **load shedding**, **rate limiting**, **token bucket shaping**, **leaky bucket shaping**, **concurrency limiting**, **adaptive concurrency limiting**, **queue depth control**, **controlled delay queue management**, **cooperative backpressure**, **cost based throttling**, **priority queueing**, **fair queueing**, **weighted fair queueing**, **deficit round robin**: decides at the entrance what may enter and in what order, at the price of rejecting work the system could have absorbed and starving low priority callers.
- **Retry discipline**, also **circuit breaking**, **retry budget**, **exponential backoff with jitter**, **retry amplification avoidance**, **jittered periodic work**, **constant work pattern**, **synchronized maintenance windows**, **background activity throttling**: bounds retries and cuts calls to a failing dependency, at the price of abandoning recoverable failures and wasted work at low load.
- **Overload and scaling laws**, also **metastable failure state**, **retry storm**, **Little's law**, **Kingman's formula**, **utilization law**, **forced flow law**, **Amdahl's law**, **Gustafson's law**, **universal scalability law**, **strong and weak scaling**, **coordinated omission**, **goodput**, **service level objective**, **USE method**: the models and measurement errors that predict when a system stays degraded after its trigger is gone and how much speedup adding workers can buy.

### Calls, copies, and consistency across machines

- **Coarsening remote calls**, also **batching remote calls**, **pipelining**, **chatty to chunky refactoring**, **remote facade**, **data transfer object**, **gateway aggregation**, **gateway offloading**, **backend for frontend**, **function fusion**: replaces many fine grained calls with fewer coarse ones, at the price of over fetching, latency for the earliest item, and a shared bottleneck.
- **Request deduplication**, also **request coalescing**, **edge request collapsing**, **duplicate suppression**, **persisted queries**: merges identical concurrent requests into one upstream call, at the price of shared fate and a registry keyed by request identity.
- **Asynchronous reply**, also **fire and forget messaging**, **asynchronous request reply**, **long polling**, **streaming responses**, **incremental payload streaming**, **queue based load leveling**: releases the caller before the work completes or delivers results as they resolve, at the price of protocol complexity, held connections, and harder retry semantics.
- **Selective responses**, also **response field selection**, **sparse fieldsets**, **pagination**, **keyset pagination**, **payload truncation by policy**, **blob externalization**, **range requests**: returns only the fields and rows a caller asked for, at the price of extra round trips, cache fragmentation, and inconsistency across pages.
- **Schema based serialization**, also **binary protocol adoption**, **variable length integer encoding**, **columnar interchange format**, **lazy deserialization**, **content negotiation**, **dictionary compression for payloads**: encodes against a declared schema instead of self describing text, at the price of schema distribution, version management, and debuggability.
- **Multi tier caching**, also **near cache**, **distributed cache**, **replicated cache**, **cache coherence across nodes**, **admission policy**, **segmented eviction**, **cache warming**, **client side response caching**: stacks caches at client, node, and service layers, at the price of multiplied invalidation paths, coordination traffic on writes, and staler reads.
- **Read routing by guarantee**, also **read replica routing**, **read your writes handling**, **session consistency routing**, **quorum size tuning**, **consistency level selection**, **bounded staleness read**, **snapshot read**, **replica lag aware routing**: sends each read to replicas current enough for the caller's guarantee, at the price of stale reads, fewer eligible replicas, and load imbalance.
- **Replication topology**, also **asynchronous**, **semi synchronous**, **chain**, **leaderless**, and **multi primary replication**, **leader locality**, **read repair**, **anti entropy repair**, **conflict free replicated data types**, **idempotent retry**, **group commit**, **batched replication**: decides who accepts writes, when they are acknowledged, and how divergence converges, at the price of data loss on failover, conflict resolution, and lag.

### Data at scale

- **Parallel phase decomposition**, also **MapReduce style decomposition**, **combiner function**, **map side aggregation**, **two phase aggregation**, **task granularity tuning**, **stage pipelining**, **dynamic executor allocation**, **external shuffle service**: expresses a job as parallel phases over partitions, at the price of a materializing shuffle between them and lost recovery points when stages fuse.
- **Join and shuffle strategy**, also **map side join**, **broadcast join**, **shuffle hash join**, **sort merge join in a cluster**, **bucketed tables**, **push based shuffle**, **spill threshold tuning**, **operator chaining**: chooses whether one side is held locally, prepartitioned, or shuffled and sorted, at the price of memory limits on the small side, skew sensitivity, and write time expense.
- **Skew handling**, also **salting of hot keys**, **range partitioning with sampling**, **hash partitioning**, **load aware repartitioning**, **skew join**, **data skew**, **hot spot**, **keyed state partitioning**: spreads a heavy key across partitions so runtime stops tracking the largest share, at the price of a second aggregation stage and a full reshuffle.
- **Adaptive query execution**, also **dynamic partition pruning**, **whole stage code generation**, **vectorized batch execution**: replans and compiles a stage from statistics observed at runtime, at the price of plan instability, compile time, and opaque debugging.
- **Checkpointing**, also **incremental checkpointing**, **unaligned checkpointing**, **changelog state replication**, **embedded state store**, **asynchronous checkpoint writing**, **sharded checkpoint writing**, **lineage based recovery**, **elastic training**: persists intermediate state so recovery need not restart from the beginning, at the price of write time, storage, and long recovery for deep lineages.
- **Precomputed results**, also **incremental recomputation**, **incremental view maintenance**, **materialized view**, **rollup table**, **precomputed cube**, **denormalization for read speed**, **write fan out**, **fan out on read**, **hybrid fan out**, **job level result caching**, **feature store precomputation**, **sketch based approximate aggregation**, **sampling based query answering**: computes an answer before it is asked, or from a bounded summary, at the price of storage, staleness, write amplification for popular producers, and bounded error.
- **Columnar storage with pushdown**, also **predicate**, **projection**, **aggregate**, and **limit pushdown**, **partition pruning**, **zone maps**, **bloom filter skipping**, **manifest based metadata**, **dictionary encoding**, **run length encoding**, **row group sizing**, **z ordering**, **sort order selection**, **compaction strategy**, **small file problem**, **tiered storage placement**, **lifecycle expiration**, **local caching of remote blocks**, **read coalescing**: stores column by column, orders rows so ranges can be skipped, and evaluates filters at the storage layer, at the price of expensive single row access, statistics maintenance, and costly rewrites.
- **Windowing and delivery guarantees**, also **tumbling**, **sliding**, and **session windows**, **watermark lateness**, **allowed lateness**, **early trigger firing**, **incremental window aggregation**, **exactly once processing**, **at least once processing**, **idempotent sink writes**, **transactional sink commit**, **dead letter offloading**, **log compaction**, **partition count sizing**, **consumer parallelism tuning**, **producer batching and linger**, **micro batching**, **zero copy log transfer**: bounds an unbounded stream so aggregation terminates and fixes how many times a record may affect the result, at the price of state per open window, retractions downstream, and transactional coordination.

### Precision, sparsity, and model size

- **Mixed precision arithmetic**, also **half precision**, **brain floating point**, **tensor float arithmetic**, **eight bit floating point**, **loss scaling**, **stochastic rounding**, **wide accumulation**, **microscaling formats**, **reduced precision collectives**: computes in reduced precision while keeping a higher precision master copy, at the price of loss scaling machinery, narrow dynamic range, and overflow risk.
- **Integer and low bit quantization**, also **eight bit integer quantization**, **four bit quantization**, **weight only quantization**, **activation quantization**, **dynamic and static quantization**, **normal float four bit**, **key value cache quantization**, **quantized embedding lookup**: represents weights and activations as narrow integers with scale factors, at the price of accuracy, calibration effort, and dequantization work inside the kernel.
- **Quantization scale placement**, also **per channel scaling**, **block wise quantization**, **group size selection**, **double quantization**, **symmetric against asymmetric quantization**, **quantization granularity**, **fused dequantization kernel**, **outlier aware quantization**, **quantized cache with high precision sinks**: chooses the scope one scale factor covers and what stays in higher precision, at the price of scale metadata volume, irregular layout, and kernel variants.
- **Calibrated and compensating quantization**, also **post training quantization**, **quantization aware training**, **GPTQ**, **AWQ**, **AdaRound**, **SmoothQuant**, **rotation based outlier suppression**, **clipping range search**, **calibration set choice**, **sensitivity analysis**, **mixed precision layer assignment**: fits quantization to observed activations, or trains through it, at the price of a calibration pass or a full training run and accuracy loss when live data shifts.
- **Codebook and extreme quantization**, also **weight clustering**, **vector quantization of weights**, **additive quantization**, **binarization**, **ternary quantization**, **outlier preserving sparse quantization**: restricts weights to a learned codebook or to one or two bits, at the price of substantial accuracy loss and decode work at inference.
- **Pruning and sparsity structure**, also **magnitude pruning**, **iterative magnitude pruning**, **movement pruning**, **second order pruning**, **lottery ticket rewinding**, **dynamic sparse training**, **unstructured**, **structured**, and **semi structured two of four sparsity**, **channel pruning**, **attention head pruning**, **depth pruning**, **activation sparsity exploitation**, **token pruning**, **token merging**, **sparse format selection**: removes parameters, channels, or tokens contributing little, at the price of accuracy, a retraining pass, and hardware that cannot exploit irregular patterns.
- **Knowledge distillation**, also **self distillation**, **intermediate feature distillation**, **distillation to a task specific student**: trains a small student to reproduce a large teacher's outputs, at the price of teacher inference passes, architectural coupling, and a lower accuracy ceiling.
- **Low rank adaptation**, also **LoRA**, **QLoRA**, **DoRA**, **VeRA**, **IA3**, **adapter tuning**, **prefix tuning**, **prompt tuning**, **BitFit**, **linear probing**, **layer freezing**, **GaLore**, **diff pruning**, **parameter efficient fine tuning**, **low rank factorization**, **tensor decomposition**, **weight tying**, **weight merging**, **model soup**, **task vector arithmetic**, **TIES merging**, **DARE**: trains or folds in a small fraction of a model's parameters instead of all of them, at the price of expressiveness, an extra product per token unless merged, and interference between merged adaptations.
- **Conditional computation**, also **mixture of experts routing**, **top k gating**, **switch routing**, **expert capacity factor**, **router load balancing loss**, **expert offloading**, **early exit network**, **cascade model**, **model routing**, **dynamic depth**, **dynamic width**, **slimmable network**, **contextual sparsity prediction**, **confidence thresholding**, **input resolution scaling**, **neural architecture search**, **once for all supernet**, **compute optimal model scaling**: activates only the part of a network an input needs, or searches for the cheapest architecture that suffices, at the price of load imbalance, irregular kernels, dropped tokens, and wrong early stops.

### Parallelism, the training step, and the kernel

- **Data parallelism**: replicates the model and splits each batch across workers, at the price of gradient synchronization every step and full model memory per worker.
- **Tensor and sequence parallelism**, also **intra layer model parallelism**, **sequence parallelism**, **context parallelism**, **ring attention**, **activation partitioning**: splits individual layer matrices or the sequence dimension across devices, at the price of collectives inside every layer and gathers to reassemble activations.
- **Pipeline parallelism**, also **inter layer model parallelism**, **interleaved schedule**, **one forward one backward scheduling**, **zero bubble schedule**, **micro batch count tuning**, **pipeline bubble**: assigns consecutive layer groups to different devices, at the price of idle fill and drain time and scheduling complexity to shrink it.
- **Expert parallelism and strategy search**, also **all to all collective**, **hybrid parallelism**, **three dimensional parallelism**, **automatic parallelization search**, **topology aware rank placement**, **collective algorithm selection**: places experts on separate devices and searches the combined split strategy, at the price of all to all routing traffic, a large configuration space, and rigid job placement.
- **Sharded optimizer state**, also **zero redundancy optimizer**, **fully sharded data parallel**, **sharding stage selection**, **factored optimizer state**, **eight bit optimizer state**, **paged optimizer state**, **parameter server architecture**: partitions parameters, gradients, and optimizer state across workers, at the price of extra collectives per step and update fidelity.
- **Offloading to host memory**, also **activation offloading**, **optimizer state offloading**, **parameter offloading**, **weight streaming**, **layer by layer weight offload**, **memory mapped weight loading**: streams state onto the accelerator only as each layer needs it, at the price of bandwidth bound steps and stalls on first touch.
- **Activation recomputation**, also **gradient checkpointing**, **selective activation recomputation**: discards activations and recomputes them during the backward pass, at the price of extra forward compute and choosing what to keep.
- **Batch composition**, also **gradient accumulation**, **micro batching in training**, **batch size scaling**, **batch size ramping**, **sequence length warmup**, **shape padding to fixed buckets**, **data echoing**, **progressive resizing**, **progressive layer stacking**, **training data deduplication**, **coreset selection**: assembles the effective batch and the curriculum that keeps devices saturated, at the price of longer wall time per step, a learning rate schedule to match, and compute spent on padding.
- **Collective efficiency**, also **ring all reduce**, **hierarchical all reduce**, **gradient bucketing**, **communication computation overlap**, **gradient compression**, **gradient quantization**, **top k gradient sparsification**, **local update averaging**, **asynchronous parameter updates**, **federated round reduction**, **federated update compression**: starts reduction before the backward pass ends and shrinks or delays what crosses the network, at the price of buffer memory, scheduling complexity, stale gradients, and convergence quality.
- **Kernel fusion and graph compilation**, also **operator fusion**, **horizontal fusion**, **epilogue fusion**, **graph compilation**, **graph capture and replay**, **training step compilation**, **just in time kernel compilation**, **kernel autotuning**, **algebraic graph simplification**, **constant folding of weights**, **batch normalization folding**, **layout optimization**, **channels last layout**, **weight prepacking**, **memory planning**, **in place operation rewriting**, **fused optimizer step**, **multi tensor apply**: captures a model as a graph and compiles fused kernels for it so intermediates never reach memory, at the price of dynamic shape support, compile time on shape changes, and small numerical differences.
- **Kernel level tiling and staging**, also **tiled matrix multiplication**, **split reduction**, **stream based reduction scheduling**, **persistent tile scheduling**, **matrix unit utilization**, **occupancy tuning**, **warp specialization**, **asynchronous bulk copy**, **double buffered shared memory**, **software pipelining**, **bank conflict avoidance**, **vectorized global loads**, **thread block clustering**, **cache residency control**, **tile and wave quantization**, **Winograd convolution**, **implicit matrix multiply convolution**, **image to column transformation**, **depthwise separable convolution**, **grouped convolution**: sizes tiles and stages them through fast memory so the matrix engines stay fed, at the price of per device tuning, register pressure, and dimension alignment constraints.

### Serving a model and retrieving from an index

- **Key value caching**, also **paged attention**, **radix tree prefix cache**, **prefix caching**, **prompt caching**, **cache eviction**, **heavy hitter eviction**, **cache offloading**, **sparse cache retrieval**, **cache aware request routing**, **cache transfer between nodes**: stores past keys and values so each new token attends without recomputing them, and shares them across requests with a common prefix, at the price of memory growing with context and batch, plus eviction and matching bookkeeping.
- **Attention shape reduction**, also **multi query attention**, **grouped query attention**, **multi head latent attention**, **cross layer key value sharing**, **sliding window attention**, **sparse attention pattern**, **linear attention**, **attention sink retention**, **tiled attention**, **online softmax**: shares or narrows what attention reads so neither the cache nor the score matrix grows with the naive shape, at the price of model quality, long range dependencies, and custom kernels.
- **Continuous batching**, also **iteration level scheduling**, **dynamic batching**, **chunked prefill**, **prefill decode disaggregation**, **sequence length aware scheduling**, **sequence bucketing**, **padding removal**, **input packing**, **token budget admission control**, **fair share token scheduling**, **preemption by swapping**, **preemption by recomputation**, **scheduler overlap with the forward pass**: adds and retires sequences from the running batch every step and admits against remaining cache, at the price of scheduler complexity, latency for the earliest arrival, and repeated prefill on preemption.
- **Speculative decoding**, also **draft model verification**, **self speculative decoding**, **multi head drafting**, **multi token prediction**, **lookahead decoding**, **prompt lookup decoding**, **tree attention verification**, **quantized draft**, **draft acceptance rate**, **constrained decoding**, **jump forward decoding**, **beam search**, **prompt compression**: proposes several tokens cheaply and verifies them in one pass of the target model, or skips tokens a grammar makes certain, at the price of wasted draft work on rejection and mask or automaton machinery.
- **Serving economics**, also **batch size tuning for throughput**, **model instance replication**, **multi model colocation**, **accelerator time slicing**, **accelerator partitioning**, **accelerator process sharing**, **speculative weight prefetch**, **semantic response caching**, **embedding cache**, **offline batch inference**, **autoscaling on queue depth**, **deadline based scheduling**, **multi adapter serving**, **adapter fusion into base weights**, **on device inference**, **neural accelerator delegation**, **graph partitioning across backends**, **split computing**: places models on devices and decides which requests share them, at the price of interference, memory pressure, wrong cache hits, and weaker isolation.
- **Approximate nearest neighbor search**, also **inverted file index**, **product quantization**, **optimized and residual quantization**, **asymmetric distance computation**, **scalar and binary quantization**, **locality sensitive hashing**, **hierarchical navigable small world graph**, **disk resident graph index**, **probe count tuning**, **search breadth tuning**, **degree bounded pruning**, **exact rescoring**, **oversampling factor**, **prefiltered and postfiltered attribute search**, **index sharding and replication**, **segment merging**, **embedding table sharding**, **hashing trick**, **matryoshka truncation**: trades exact results for sublinear retrieval, at the price of recall, index build time, and memory for the structures that buy it back.
- **Two stage ranking**, also **reranking cascade**, **two stage candidate generation**, **late interaction retrieval**, **dynamic pruning**, **WAND**, **block max WAND**, **MaxScore**, **document at a time scoring**, **term at a time scoring**, **impact ordered postings**, **skip pointers**, **static index pruning**, **tiered index**, **document reordering**, **block compressed gap encoding**, **Elias Fano encoding**, **roaring bitmap postings**, **posting list caching**, **query result caching**, **reciprocal rank fusion**: retrieves candidates cheaply and rescores a shortlist with an expensive model, skipping anything unable to enter the top results, at the price of recall lost in the first stage and per term bound bookkeeping.
- **Serving measures**, also **time to first token**, **inter token latency**, **tokens per second**, **cost per token**, **memory bandwidth bound decoding**, **effective batch utilization**, **model FLOPs utilization**, **hardware FLOPs utilization**, **roofline analysis**, **arithmetic intensity**, **memory bound against compute bound classification**, **operator level profiling**, **queries per second at fixed recall**: the quantities that say whether a deployment is limited by reading weights, by arithmetic, or by the batch it manages to fill.

## Measuring, and deciding what to do

### Deciding whether to act

- **Premature optimization**, also **the root of all evil**: tuning code for speed before measurement or requirement has shown that code to be critical, spending clarity on speed nobody needs.
- **Premature pessimization**: choosing a gratuitously slower construct where an equally clear and equally simple faster one exists, conceding speed that cost nothing to keep.
- **The rules of optimization**: Jackson's pair, that rule one is do not do it and rule two is do not do it yet, at the price of shipping known slowness.
- **Make it work, make it right, make it fast**: staged ordering that forbids tuning until behaviour is correct and the code is clean, at the price of late discovery of structural faults.
- **Correctness before speed**: refusing any speed gain that trades away a correct result, at the price of approximations that would have been good enough.
- **Measure, do not guess**: no optimization proceeds without a measurement naming its target, at the price of the tooling and the time each measurement demands.
- **Fix the design before tuning the code**: correcting structural bottlenecks at the architecture level, since code tuning cannot repair them, at the price of expensive late redesign.
- **Software performance engineering**, also **SPE**: building performance into design through quantitative objectives and models rather than tuning afterwards, at the price of modelling effort before any code runs.
- **The optimization stage approach**: writing the whole program for clarity and reserving a distinct later phase for measured optimization, at the price of unknown performance until that phase arrives.
- **The constant attention approach**: keeping performance in view during every change instead of reserving a tuning phase, at the price of continual small concessions in clarity.
- **Good enough performance**, also **fast enough is fast**: stopping once the stated requirement is met rather than pursuing the fastest possible, at the price of headroom against future load.
- **Opportunity cost of optimization**, also **Rule of Economy**: engineering hours rather than machine cycles decide what gets optimized, at the price of machine efficiency deliberately left unclaimed.

### Where to aim the effort

- **Bottleneck first discipline**: working only on the single dominant constraint, then re-measuring to find the next, at the price of ignoring cumulative small costs.
- **Theory of constraints**, also **the five focusing steps**: Goldratt's doctrine that one binding constraint sets throughput, worked by identify, exploit, subordinate, elevate, and repeat, at the price of restarting the analysis after each success.
- **Bottleneck shift**: the movement of the binding constraint onto another resource once the first is relieved, which ends the gain after a single step.
- **Amdahl guided prioritization**: bounding the payoff of a local speedup by the fraction of total time it occupies, at the price of discouraging work with real but small returns.
- **Hot spot discipline**, also **the ninety ten rule** and **the Pareto principle**: concentrating effort where measurement shows time concentrating, at the price of blindness to waste spread thinly.
- **Optimize the common case**, also **handle normal and worst case separately**: giving the frequent path a specialized route while rare cases take a slower general one, at the price of two paths to keep correct.
- **Algorithmic improvement before micro-optimization**: changing asymptotic cost before tuning constants, at the price of rewriting working, understood code.
- **Optimize the wait, not the work**: reducing the time a user perceives as waiting rather than the computation performed, at the price of resource consumption unchanged or higher.

### The named rule sets

- **Bentley's rules for writing efficient programs**: a numbered catalog of code tuning rules grouped under space for time, time for space, loops, logic, procedures, and expressions, at the price of rules calibrated to the machines of 1982.
- **Lampson's hints for computer system design**: a numbered collection of design hints sorted by functionality, speed, and fault tolerance, whose speed hints cover caching, batching, and shortcuts, at the price of terseness that demands judgement.
- **Kernighan and Plauger's efficiency rules**: the numbered style rules governing when tuning starts and how far it goes, from make it right before you make it faster to let the compiler do the simple optimizations, at the price of speed reachable only by breaking their order.
- **Do not diddle code to make it faster, find a better algorithm**: the rule preferring asymptotic change to local fiddling, at the price of larger and riskier rewrites.
- **Pike's rules of programming**: five numbered rules holding that cost sits where nobody expects, that it must be measured, and that simple algorithms on well chosen data beat clever ones, at the price of asymptotic headroom on inputs that grow.
- **You cannot tell where a program spends its time**, also **Pike's first rule**: bottlenecks sit in surprising places, so intuition is never evidence, at the price of the speed of acting on a hunch.
- **Data dominates**, also **representation is the essence of programming**: the choice of data structure decides performance, so representation is designed first, at the price of churn when the representation must change.
- **Kernighan's law**: debugging is twice as hard as writing code, so cleverness beyond one's debugging ability is unaffordable, at the price of the speed only clever code reaches.
- **Smith's performance principles**: the numbered engineering principles placing work near its data and minimizing the dominant workload's processing, covering centering, locality, fixing point, processing versus frequency, shared resources, and spreading the load, at the price of a model per principle before design.
- **Gregg's performance mantras**: the ordered ladder of do not do it, do it no more than once, do it less, do it later, do it out of sight, do it concurrently, and do it more cheaply, at the price of a different resource surrendered at each rung.

### Working out where the time goes

- **The problem statement method**: interrogating what is slow, since when, and what changed before measuring anything, at the price of questioning that delays the first data.
- **The scientific method applied to performance**, also **the diagnosis cycle**: forming a falsifiable hypothesis about the bottleneck and iterating instrumentation and data until the cause is isolated, at the price of an open ended number of rounds.
- **The USE method**: checking utilization, saturation, and errors for every resource in turn, at the price of a complete resource inventory with metrics for each.
- **The RED method and the four golden signals**: examining rate, errors, and duration for each service, and latency, traffic, errors, and saturation for each user facing system, at the price of a saturation signal required per resource.
- **Drill down analysis**, also **latency drill down**: peeling one layer at a time and apportioning the measured latency at each step, at the price of consistent instrumentation at every layer crossed.
- **Method R**: identifying the operation the user cares about, decomposing its response time by component, and attacking the largest component, at the price of per operation trace data.
- **Workload characterization**: describing who applies the load, why, of what it consists, and how it changes, at the price of substantial observation that examines no component.
- **Back of the envelope estimation**, also **napkin math**: predicting achievable performance from a few known constants before measuring, at the price of accuracy traded for speed of judgement.
- **Latency numbers by order of magnitude**: the memorized table of typical costs from register access to network round trip, used to sanity check any estimate.

### Ways of finding a cost

- **Sampling profiler**, also **statistical profiling**: interrupts execution periodically and records the stack, building a statistical picture of cost, at the price of missing short lived events and of error on rarely taken paths.
- **Instrumenting profiler**, also **deterministic profiling**: records every event of interest exactly rather than sampling, at the price of per call overhead that distorts the timings measured and suppresses inlining.
- **Event based sampling**: triggers each sample after a fixed count of hardware events rather than from a timer, at the price of attribution skid near the triggering instruction.
- **Precise event based sampling**, also **PEBS** and **instruction based sampling**: hardware records the exact state for a sampled event, or the whole latency breakdown of one tagged instruction, at the price of specific processor support.
- **Wall clock profiling versus CPU profiling**: sampling every thread whatever its state against sampling only threads on a processor, the first charging idle waiting as work and the second hiding it entirely.
- **Line and instruction level attribution**: attributing samples to single source lines or machine instructions rather than to whole functions, at the price of skid, higher overhead, and results tied to one build.
- **Event tracing**: recording individual timestamped events rather than aggregates, at the price of data volume and overhead that rise with the event rate.
- **Static instrumentation**, also **tracepoint** and **USDT probe**: measurement points compiled in ahead of time with a stable event format, at the price of committing to a probe as an interface.
- **Dynamic instrumentation**, also **kprobe** and **uprobe**: measurement patched into running code on demand, at the price of privilege, a trap per hit, and fragility across versions of the target.
- **Continuous profiling in production**: collecting low frequency profiles from the live system permanently, because test systems misrepresent it, at the price of steady overhead and of risk borne by real users.

### Reading a profile

- **Self time and total time**, also **exclusive and inclusive cost**: the paired accounting that separates a function's own instructions from the work it triggered.
- **Flat profile and call graph profile**: a ranking of functions by measured cost against a profile that records caller and callee relations so cost propagates to callers.
- **Calling context tree**: a call tree keeping each distinct chain of callers separate, so cost is attributed per context rather than per function.
- **Flame graph**: a stacked visualization whose box width is aggregated cost and whose vertical depth is stack depth, ordered alphabetically rather than in time.
- **Flame chart**: a stack visualization whose horizontal axis is wall clock progress, showing when work happened rather than how much of it there was.
- **Differential flame graph**: a flame graph coloured by the signed difference between two profiles, showing where cost moved between them.
- **Off CPU flame graph**: a flame graph of blocked time, aggregating stacks at the moment threads left the processor.

### Measuring the machine underneath

- **Hardware performance counter**, also **PMU**: the on chip registers that count and sample microarchitectural events such as cycles, misses, and retired instructions.
- **Instructions per cycle**, also **IPC** and **CPI**: retired instructions per core cycle and its reciprocal, the standard scalar summary of pipeline efficiency.
- **Top down microarchitecture analysis**, also **TMAM**: hierarchical cycle accounting that splits issue slots into retiring, bad speculation, front end bound, and back end bound, then refines the dominant one, at the price of vendor specific event support.
- **Memory bound versus core bound**: the split of back end loss between waiting on the cache and memory hierarchy and pressure on execution ports.
- **Bad speculation**, also **wasted work**: the share of issue slots consumed by work later discarded, from branch mispredictions and pipeline clears.
- **Misses per kilo instruction**, also **MPKI**: cache or predictor misses normalized per thousand retired instructions, comparable across workloads of different length.
- **Last level cache miss ratio**: the fraction of last level cache accesses that go to memory, the strongest single predictor of memory boundedness.
- **Cache line contention measurement**, also **HITM measurement**: counting loads served from another core's modified line, the direct signature of sharing between threads and of false sharing.
- **Memory bandwidth and latency measurement**: quantifying bytes per second moved and the load to use delay at each level, at the price of uncore counters and of pointer chasing patterns that defeat prefetch.

### Measuring waiting and memory

- **Off CPU analysis**: measuring the time threads spend blocked and the stacks at which they blocked, at the price of tracing every scheduler switch.
- **Run queue latency**, also **scheduler latency**: the delay between a thread becoming runnable and being dispatched, the direct signal of processor saturation.
- **Lock contention profiling**: attributing wait time to acquisition sites and to the holders that caused it, separating how long a section is held from how long acquirers blocked, at the price of instrumenting every lock operation.
- **Spin time measurement**: measuring cycles burned in adaptive spinning before a thread parks, which appears as processor work and is pure loss.
- **CPU steal time**: processor time the hypervisor gave to another guest, invisible inside the guest and fully charged to its wall clock.
- **Allocation profiling**: recording the size and site of allocations, sampled by size weight where the rate is high, at the price of overhead proportional to the allocation rate.
- **Heap profiling with retention analysis**: attributing live heap to allocation sites and computing which objects exclusively keep each subgraph alive, at the price of snapshot pauses and expensive graph analysis.
- **Garbage collection pause measurement**: recording the duration and distribution of stop the world phases and the share of wall clock left to application code, at the price of runtime logging.
- **Resident set size**, also **RSS**: the physical memory currently resident for a process, whose high water mark decides whether a workload fits.

### Following one request across boundaries

- **Distributed tracing**: following one request across process boundaries as a causally linked set of spans, at the price of context propagation plumbing in every hop.
- **Span and trace**: one timed unit of work carrying a name, timestamps, and attributes, and the set of spans sharing a trace identifier.
- **Exclusive span time**: the portion of a span's duration not covered by its children, the distributed analogue of self time.
- **Critical path analysis in a trace**: identifying the chain of spans whose durations actually set the response time, at the price of complete and clock aligned spans.
- **Head based versus tail based sampling**: deciding at a trace's start whether to record it against buffering whole traces and keeping the interesting ones, the first discarding what turns out to matter and the second demanding memory at a collector that sees every span.
- **Exemplar**: a trace identifier attached to an aggregated metric sample, so a percentile can be opened into one concrete request.
- **Real user monitoring versus synthetic monitoring**: timing collected from actual client sessions against repeated exercise from controlled probes, the first noisy and uncontrolled and the second a scripted path rather than real behaviour.

### The vocabulary of rate, delay, and utilization

- **Latency and response time**: the time from initiating an operation to its completion, response time comprising queueing delay plus service time.
- **Service time versus response time**: the distinction whose confusion makes a saturated system look fast, since service time hides the queue in front of it.
- **Throughput and goodput**: completed work per unit time, and the share of it that was useful once retransmissions, retries, and discarded results are removed.
- **Utilization**: the fraction of an interval a resource was busy, or the fraction of its capacity in use, the two disagreeing once a resource is always busy and not yet full.
- **Saturation**: the degree to which work is queued beyond a resource's ability to serve it, the metric that keeps rising after utilization has reached its ceiling.
- **Concurrency**: the number of requests in the system at once, the quantity that links throughput and latency.
- **Round trip time**, also **RTT**: the time for a signal to reach a peer and its acknowledgement to return, the floor under any request on that path.
- **Cost per request**, also **CPU seconds per request**: the monetary and processor cost of one unit of work, the figures that make efficiency comparable to spend.
- **Performance per watt and the energy delay product**: work completed per unit of power, and energy multiplied by time, the second refusing to buy power savings with unbounded delay.

### Percentiles, tails, and service levels

- **Latency percentile**: the value below which a stated proportion of measured latencies fall.
- **Median versus mean latency**: the latency exceeded by half of requests against the arithmetic average, the second hiding multimodality and the tail that users notice.
- **Tail latency**, also **p99** and **p999**: the slow end of the distribution, summarized by the latency exceeded by one request in a hundred or in a thousand, where the requests that define user experience live.
- **Percentile of percentiles fallacy**: averaging or taking percentiles of already computed percentiles, which yields a figure corresponding to no real request.
- **Percentile aggregation across windows**: summing or averaging per interval percentiles, which understates the true tail of the combined period.
- **Latency histogram**: counts of measurements per latency bucket, preserving the distribution's shape, with logarithmic or exponential buckets holding relative error constant across magnitudes.
- **Jitter and latency outliers**: the variability of latency across successive operations, and individual measurements far above the body of the distribution, usually caused by a pause rather than by extra work.
- **Service level indicator, objective, and agreement**: the precisely defined measurement, the target it is required to meet, and the contractual commitment whose breach carries consequences.
- **Error budget and burn rate**: the permitted shortfall against an objective over a window, spendable on risk and change, and the speed at which current failures consume it.

### Building a benchmark

- **Microbenchmark**: times a single small operation in isolation, at the price of results that need not predict behaviour inside a real program.
- **Macrobenchmark**: times a whole realistic workload end to end, at the price of poor attribution when the number moves.
- **Warmup and steady state measurement**: discarding initial iterations and measuring only once performance has stopped changing, at the price of hiding exactly the startup behaviour some users pay.
- **Sink function**, also **blackhole** and **optimization barrier**: consumes a result or blocks code motion so the compiler cannot delete the measured work, at the price of overhead and of inhibiting optimizations the real program would get.
- **Baseline measurement**: establishing the current number before any change so improvement can be claimed, at the price of a full measurement cycle that yields no gain.
- **Paired and interleaved comparison**: alternating the variants under test under identical conditions so environmental drift affects both equally, at the price of doubled measurement time and scheduling complexity.
- **Open loop versus closed loop load generation**: issuing requests at a chosen arrival rate against a fixed population each waiting for its previous response, the first growing queues without bound and the second self throttling so overload never shows.
- **Ramp load method**, also **knee detection**: raising load in steps to locate where response time turns sharply upward against throughput, at the price of a long controlled run.
- **Active benchmarking**: analysing the system with other tools while the benchmark runs to confirm what it actually limits, at the price of much slower iteration.

### Comparing two measurements

- **Repeated trials and run to run variance**: measuring many times so the spread that bounds the smallest detectable change is known, at the price of measurement time multiplied by the trial count.
- **Independent replication**: repeating in fresh processes on fresh machine state so run level variation enters the estimate, at the price of many more runs.
- **Confidence interval and prediction interval**: the range expected to contain the true value, and the range expected to contain the next single measurement.
- **Minimum detectable effect and statistical power**: the smallest difference a given experiment can resolve, and the probability it detects a real regression of a stated size.
- **Heavy tailed latency and the normality assumption**: latency is bounded below and skewed right with frequent extremes, so tests and summaries assuming a normal distribution misreport it.
- **Nonparametric comparison**, also **Mann Whitney U test** and **Kolmogorov Smirnov test**: comparing measured samples without assuming a distribution, at the price of lower power and of silence about which region of the distribution moved.
- **Ratio averaging fallacy**: averaging speedup ratios arithmetically rather than geometrically, which weights the results wrongly and can invert the conclusion.
- **Multiple comparisons problem**: false positives inflating when every benchmark in a large suite is tested for regression at once, corrected by dividing the threshold at the cost of missing small true regressions.

### What a measurement gets wrong

- **Coordinated omission**: a load generator that waits for a slow response stops issuing requests, so the delays those requests would have suffered are never recorded.
- **Survivorship in measurement**: computing latency only over requests that completed, excluding the timeouts that were the worst cases.
- **Instrumentation gap**: latency accumulating in a stage nobody instrumented, so the measured parts sum to less than the observed whole.
- **Probe effect**, also **observer effect**: measurement perturbing the system measured, with cost falling unevenly so that frequently called small functions look expensive.
- **Safepoint bias and missing inlined frames**: managed runtimes sampling only at safepoints and inlined callees vanishing from stacks, both moving cost onto innocent code.
- **Attribution skid and sampling aliasing**: a sample landing later than the instruction that caused the event, and a sample interval beating against a periodic workload so some phases are never seen.
- **Benchmark elision by the compiler**: dead code elimination, constant folding, and loop hoisting removing the measured computation, so an empty loop is timed.
- **Measurement bias**: systematic distortion from an innocuous experimental choice such as link order, code layout, allocation addresses, or stack alignment.
- **Machine level interference**: variance from noisy neighbours, sibling hardware threads, container quota throttling, turbo, and thermal drift, which changes the clock and the cache a run receives.
- **Unrepresentative measurement**: cold caches and first run costs presented as steady state, input whose size or distribution differs from production, and a conclusion drawn from one host.

### Laws that bound the gain

- **Amdahl's law**, also **the serial fraction**: speedup from accelerating part of a computation is bounded by the fraction that part occupied, so the serial remainder caps the gain.
- **Gustafson's law**: with problem size scaled to the processor count, achievable speedup grows nearly linearly because the parallel portion grows with the machine.
- **Karp Flatt metric**: the serial fraction computed from measured speedup and processor count, which exposes parallel overhead that Amdahl's own fraction hides.
- **Strong and weak scaling**: holding total problem size fixed while adding processors against holding per processor size fixed, the first measuring how far time to solution falls and the second whether it stays constant.
- **Work span model**, also **Brent's theorem** and **the critical path**: total work and the longest chain of dependent operations bound achievable time, which is at least work divided by processors plus the span.
- **Universal scalability law**: throughput as a function of concurrency bounded by a contention term and a coherency term, predicting a peak followed by retrograde decline as concurrency grows.
- **Memory wall**: the widening gap between processor speed and memory latency, which makes data movement rather than arithmetic the limit on speed.
- **Power wall**, also **the free lunch is over**: the power and thermal ceiling that ended clock frequency growth, made performance per watt governing, and moved further gains to explicit concurrency.
- **Wirth's law**: software grows slower faster than hardware grows faster, so each hardware gain is consumed by the software that follows it.
- **Tail at scale**: fanning one request out to many servers makes its latency track the slowest respondent rather than the median.

### Queueing results, and how a queue fails

- **Little's law**: the mean number of items in a stable system equals the mean arrival rate multiplied by the mean time each spends in it.
- **The operational laws**: utilization equals throughput multiplied by service demand, each resource's throughput equals system throughput multiplied by its visit count, and response time equals users divided by throughput minus think time.
- **Service demand law**: a resource's service demand equals its utilization divided by system throughput, which makes demand measurable without touching the resource.
- **Kingman's formula**: mean wait grows with utilization over one minus utilization and with the variability of both arrivals and service.
- **Coefficient of variation of service time**: the normalized variability of service durations, the term that makes waiting explode well below full utilization.
- **The knee of the curve**, also **the utilization target**: the utilization beyond which small increases in load produce large increases in wait, which is why an operating point is chosen below saturation.
- **Pooling and the square root staffing rule**: one shared multi server queue waits far less than separate queues, with servers needed equal to the offered load plus a multiple of its square root.
- **Head of line blocking**, also **the convoy effect**: one blocked or slow item at the front of a shared queue or connection delaying all the ready work behind it.
- **Bufferbloat**: latency inflation from oversized buffers holding a standing queue, which leaves throughput intact while response time collapses.
- **Thundering herd**, also **cache stampede** and **retry amplification**: many waiters released, many entries expiring, or many layers retrying at one instant, so duplicated work arrives together on the resource least able to take it.
- **Congestion collapse and the metastable failure state**: offered load climbing while useful throughput falls toward zero, sustained by its own retry and queue feedback after the trigger has gone.

### Keeping a gain from rotting

- **One change at a time**: making a single alteration between measurements so causation is attributable, at the price of a much longer optimization cycle.
- **Measure again after changing**, also **revert on no improvement**: re-running the same measurement to confirm the predicted gain and backing the change out when it fails to appear, at the price of discarded work.
- **Continuous benchmarking**: running the benchmark suite on every change and tracking the series, at the price of dedicated stable hardware.
- **Performance regression gate**, also **the performance ratchet**: blocking a change that crosses a threshold or worsens the best measured result, at the price of false failures from measurement noise stalling delivery.
- **Change point detection and performance bisection**: locating the moment a metric series shifted level, then binary searching the commit range by measurement, at the price of a full measurement run per step.
- **Automated canary analysis with guardrail metrics**: comparing a canary's metrics against a baseline statistically, watching latency and cost while a change pursues its own target, at the price of thresholds that need tuning.
- **Keep the naive implementation and test against it**: retaining the simple version as reference, fallback, and documentation, and treating any divergence on identical inputs as a defect, at the price of two implementations kept in step forever.
- **Guard the invariant the trick assumes**: asserting or type encoding the precondition a fast path depends on, at the price of the check's own runtime and code weight.
- **Document the measurement**, also **comment the trick**: recording beside the code the numbers, conditions, and reasoning that justified an optimization, at the price of records that must be refreshed as hardware changes.
- **Software aging and rejuvenation**: the performance decay of a long running process from leaks, fragmentation, and accumulated state, answered by scheduled restarts at the cost of downtime and cold caches.

### Failure modes of optimization practice

- **The streetlight anti-method**: examining whatever metric is familiar or convenient rather than the one the problem requires, then changing things until the symptom passes.
- **The random change anti-method**, also **shotgun debugging**: guessing at edits and keeping whatever coincides with an apparent improvement, so noise is credited as cause and unexplained configuration accumulates.
- **The blame someone else anti-method**: attributing a problem to another team or component without evidence, which relocates the investigation instead of advancing it.
- **The traffic light anti-method**, also **the watermelon metric** and **the vanity metric**: judging health by dashboards and impressive numbers whose thresholds report green while the experience beneath them is poor.
- **Passive benchmarking**: accepting a benchmark's number without investigating what limited it, so something other than the intended subject is routinely measured.
- **Benchmarking crimes**: the catalog of recurring methodological faults that invalidate a published evaluation, from improper baselines and selective data sets to relative numbers only, missing platform specifications, and no indication of significance.
- **Benchmarketing**: reporting results selected and configured to sell a product rather than to describe its behaviour, which independent repetition does not reproduce.
- **Goodhart's law**, also **teaching to the test** and **benchmark overfitting**: once a measure becomes the target it stops standing for what it measured, and tuning raises the score while the real workload gains nothing.
- **The fallacy of the local optimum**: improving a component in isolation while the whole system stays unchanged or slows.
- **Cargo cult optimization**, also **tuning by folklore** and **voodoo constants**: copying another project's optimization without its measurements, applying rules inherited from older hardware, and keeping knobs nobody can justify.
- **Analysis paralysis**: extending measurement and modelling indefinitely, so no performance change is ever made.

### Proving an optimization correct

- **Differential testing**: runs two implementations on identical inputs and treats any divergence as a defect, at the price of building and running both.
- **Property based testing of an optimization**: asserts invariants over generated inputs rather than fixed cases, at the price of generator design and nondeterministic failures.
- **Metamorphic testing**: checks that related inputs produce the expected relation between outputs where no oracle exists, at the price of devising sound relations.
- **Fuzzing an optimized path**: drives the fast path with random and adversarial inputs to find cases it mishandles, at the price of compute and triage effort.
- **Golden output comparison**: freezes a known good output and diffs every optimized run against it, at the price of baselines that break on legitimate change.
- **Equivalence checking**, also **correctness proof for a clever trick**: verifies mechanically or by proof that a tuned routine computes the same function as its reference, at the price of limits on tractable size.
- **Coverage of the slow path**: ensures tests exercise the fallback as well as the fast route, at the price of cases that must be constructed artificially.

### Living with the compiler

- **Do not fight the optimizer**, also **trust the compiler** and **hand tuning versus compiler trust**: leaves routine transformation to the toolchain, since hand transformations obstruct its analysis, at the price of control over the generated code.
- **Write code the optimizer understands**: shapes loops and aliasing so the compiler can prove what it needs to transform them, at the price of natural expression.
- **Verify the compiler**, also **check the optimization report**: reads the generated assembly and the compiler's own account of which loops it vectorized or refused, at the price of the skill each inspection demands.
- **Do not rely on unspecified optimization**: writes code that stays correct and fast enough when a hoped for transformation does not occur, at the price of that transformation's gain.
- **The zero overhead principle**, also **zero cost abstraction**: Stroustrup's rule that unused features cost nothing and used ones could not be hand coded better, at the price of language and implementation complexity.
- **Premature assembly**: dropping to hand written machine code before establishing that the compiler's output is the limiting factor.
- **Optimization flag discipline**: fixes and records the settings a build uses so measurements and shipped artifacts correspond, at the price of freedom to tune per module.
- **Compile time as a budget**: treats build duration as a cost limiting how much optimization a project can afford, at the price of runtime speed foregone.

### Clocks and the machine under a measurement

- **Monotonic clock use**: times intervals with a clock that never steps backwards, at the price of values carrying no relation to calendar time.
- **Time stamp counter**, also **TSC** and **invariant time stamp counter**: a per core cycle counter read by one cheap instruction, the invariant form ticking at a fixed rate whatever the core's frequency.
- **High resolution timer against coarse clock**: nanosecond resolution bought with an expensive read path, against a value cached once per tick that reads almost free.
- **Serializing barrier before timing**: forces instruction completion before a counter read so out of order execution cannot skew a short interval, at the price of overhead per read.
- **User time and system time**: the split of processor time between the program's own instructions and kernel work performed on its behalf.
- **Process time accounting**, also **tick based accounting**: reads accumulated usage from the operating system instead of timing externally, at the price of tick resolution that misattributes short lived work.
- **Timer wheel resolution**: the granularity at which a timer subsystem schedules expiries, which floors any timeout driven measurement.
- **Fixing the machine for measurement**, also **processor pinning**, **frequency fixing**, and **isolated core measurement**: binds the measured thread to a reserved core and locks the clock rate, at the price of concealing scheduler effects and production power behaviour.

### Named tests, and the gates that hold a gain

- **Volume testing**: exercises the system against production scale data so plans and structures that degrade only when large are exposed, at the price of building that data.
- **Configuration testing**: measures one workload across configuration variants to find which settings actually matter, at the price of a combinatorial test matrix.
- **Isolation testing**: repeats a narrowed test to confirm and locate one suspected bottleneck, at the price of results no longer reflecting a real mix.
- **Performance smoke test**: runs a short fixed workload on every build to catch gross regressions early, at the price of missing anything subtle.
- **Latency injection**: delays a dependency deliberately in a live system to observe timeout, retry, and budget behaviour, at the price of harming real requests.
- **Operational profile**: a quantified description of how users exercise each function, used to weight a test toward real usage, at the price of survey effort.
- **Error budget policy**: the agreed rule for what happens once a budget is spent, such as freezing feature work, at the price of negotiating enforcement in advance.
- **Multiwindow multi burn rate alerting**: alerts on budget consumption over a short and a long window together so fast and slow burns both fire, at the price of configuration complexity.
- **Production readiness review**: a checklist review of capacity evidence, load results, and objectives before a service takes real traffic, at the price of delay before launch.

### Antipatterns with proper names

- **The N plus one query problem**: issuing one query per element of a result set instead of retrieving the whole set in a single query.
- **Extraneous fetching**, also **Sisyphus database retrieval**: retrieving more rows, columns, or fields than the operation uses, then discarding the surplus.
- **Empty semi trucks**, also **chatty interface**: a boundary crossed by very many small calls where few large ones would carry the same data.
- **Circuitous treasure hunt**: reaching data through a chain of lookups, each fetch supplying only the key for the next.
- **Tower of Babel**: converting data between formats repeatedly as it crosses component boundaries.
- **One-lane bridge**, also **extensive processing**: a point admitting one process at a time, or a long step on a shared path, forcing everything else to queue.
- **Unbalanced processing**, also **pipe and filter** and **concurrent processing systems**: the slowest stage fixing every other stage's throughput while available processors sit idle.
- **Busy database**, also **monolithic persistence**: processing pushed into the data store until the dearest tier to scale is the bottleneck, with unlike access patterns sharing it.
- **Busy front end**, also **synchronous input output**: request serving threads occupied by background work or blocked awaiting slow calls, so concurrency caps at thread count.
- **Improper instantiation**, also **excessive dynamic allocation**: recreating objects meant to be shared, or churning short lived ones, until setup and allocation dominate useful work.
- **The ramp**, also **traffic jam**: processing time growing as data and state accumulate, and a queue persisting long after the spike or slow stage that made it.
- **Are we there yet**, also **is everything okay** and **where was I**: polling for a condition instead of being notified, checking status faster than it can change, and rebuilding context every interaction.

### Energy, carbon, and cost figures

- **Energy to solution**: the total energy a complete job consumes, exposing idle draw across long runs that per operation figures hide.
- **Performance per dollar**: work completed per unit of money spent, the figure that decides between faster hardware and more of it.
- **Embodied carbon**: the emissions from manufacturing and retiring the hardware a workload occupies, charged against it alongside its operational energy.
- **Facility effectiveness ratios**, also **PUE**, **CUE**, and **WUE**: total facility power, emissions, and water divided by the energy delivered to computing equipment.
- **Demand shifting**: moves flexible work to a time or region where the electricity supply is cleaner, at the price of latency and scheduling machinery.
- **Demand shaping**: cuts the work a system asks for when clean supply is scarce, such as lowering fidelity, at the price of degraded output.
- **Hardware efficiency**: draws more work from fewer devices so embodied carbon amortizes, at the price of consolidation risk and pressure to run near saturation.

### Real time timing analysis

- **Worst case execution time**, also **WCET** and **best case execution time**: proven upper and lower bounds on a path's execution time on given hardware, the pair that also bounds jitter.
- **Response time analysis**: the schedulability test computing each task's worst case response time including interference from every higher priority task.
- **Liu and Layland bound**: the result that rate monotonic scheduling meets every deadline while total utilization stays below about sixty nine percent.
- **Deadline miss ratio**: the fraction of activations finishing after their deadline, the tolerance metric for soft real time work.
- **Timing anomaly**: the effect where a locally faster event produces a globally longer execution, which breaks naive composition of worst cases.
- **Measurement based timing analysis**: bounds execution time from observed runs plus a safety margin rather than from a processor model, at the price of unsound bounds on unexercised paths.

### How long a wait feels

- **Just noticeable difference in duration**: the smallest change in a wait a person detects, roughly a fifth of the original duration, below which tuning goes unnoticed.
- **Psychology of waiting lines**: Maister's account of why occupied, explained, and bounded waits feel shorter than idle, unexplained, open ended ones, at the price of no reduction in real time.
- **Law of service**: Maister's rule that satisfaction equals perception minus expectation, so managing expected latency substitutes for cutting it, at the price of trust when expectations are set falsely.
