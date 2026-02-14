# Hybrid Optimization for Deterministic Ambulance Routing in Healthcare Logistics

This project presents a hybrid optimization approach for the **Ambulance Routing Problem (ARP)**, where every second counts for patient survival.  

## Project Overview
Optimize ambulance routes to minimize response times and maximize coverage of critical cases using:  
- **Exact Methods (MILP)**: IBM ILOG CPLEX for small instances to provide benchmark solutions.  
- **Metaheuristics**: GA, TS, SA, ACO for large-scale, real-world scenarios (up to 3,000 calls).  

## Mathematical Model
The ARP is formulated as a **Mixed-Integer Linear Program (MILP)** with three objectives:  
- **Z1**: Minimize total travel distance  
- **Z2**: Minimize average response time  
- **Z3**: Maximize coverage of urgent cases  

Constraints include flow conservation, time windows, maximum route duration, and mandatory return to depot.  

# Experimental Results – Ambulance Routing Problem (ARP)

This project evaluates **exact optimization (MILP)** and **metaheuristic approaches** for solving the Ambulance Routing Problem in EMS networks.

## Experimental Setup
- Tested on **small (≤15 calls)**, **medium**, and **large (≤3,000 calls)** instances.  
- **Exact optimization (CPLEX)** is used for small-scale instances (limited to ~1,000 variables/constraints).  
- **Metaheuristics (GA, TS, SA, ACO)** handle medium and large-scale scenarios.  

## Performance Metrics
- **Total Distance (km):** Sum of all ambulance travel.  
- **Average Response Time (min):** Mean arrival time at emergencies.  
- **Critical Coverage (calls):** Number of emergencies served within the critical time threshold.  
- **Computational Time (s):** Time to generate solutions.  

## Key Results

### Exact Optimization (Small Instances)
- **CPLEX** achieves global optimality with negligible computation time (0.06 s).  
- Low average response (11.17 min) and full critical coverage (10 calls).  

### Metaheuristics – Small Instances (10 calls)
| Algorithm | Distance (km) | Avg Response (min) | Critical Coverage | Comp Time (s) |
|-----------|---------------|------------------|-----------------|---------------|
| GA        | 67.38         | 26.91            | 9               | 0.0024        |
| TS        | 24.74         | 12.61            | 10              | 0.0186        |
| SA        | 63.16         | 30.33            | 8               | 0.0071        |
| ACO       | 51.49         | 18.96            | 10              | 0.0093        |

### Metaheuristics – Medium/Large Instances (3,000 calls)
| Algorithm | Distance (km) | Avg Response (min) | Critical Coverage | Comp Time (s) |
|-----------|---------------|------------------|-----------------|---------------|
| GA        | 24,579.27     | 508.35           | 172             | 0.91          |
| TS        | 25,035.36     | 516.23           | 154             | 2.66          |
| SA        | 25,338.36     | 520.79           | 153             | 0.13          |
| ACO       | 24,888.31     | 525.17           | 155             | 0.93          |

## Insights
- **Exact Optimization:** Optimal for small instances, balancing travel efficiency, response time, and critical coverage.  
- **Metaheuristics:** Efficient for large-scale EMS; each algorithm shows trade-offs between distance, response, and coverage.  
  - **GA:** Maximizes overall critical coverage.  
  - **TS & SA:** Prioritize fast response, benefiting urgent “red” cases.  
  - **ACO:** Balances travel distance and timely service.  
- **Trade-offs:** Metaheuristics provide flexible near-optimal solutions with minimal computation.  

## Operational Takeaways
- The MILP model ensures patient prioritization even when using metaheuristics.  
- Exact methods serve as benchmarks, while metaheuristics handle real-world, large-scale EMS scenarios.  
- Future work could explore **hybrid approaches**, combining exact optimization for subproblems with metaheuristics for scalability.  

## Conclusion
Hybrid optimization combines mathematical rigor and practical applicability. **GA** proves robust for managing emergency logistics in dense urban environments.
