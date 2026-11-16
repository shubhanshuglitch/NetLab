from typing import Dict, List, Any, Tuple, Optional
import networkx as nx


def calculate_dijkstra(nodes: List[str], links: List[Dict[str, Any]], source: str) -> Dict[str, Any]:
    """
    Computes step-by-step Dijkstra's Shortest Path Algorithm for interactive learning.
    links: [{"source": "R1", "target": "R2", "cost": 10}, ...]
    """
    G = nx.Graph()
    for n in nodes:
        G.add_node(n)
    for l in links:
        G.add_edge(l["source"], l["target"], weight=float(l.get("cost", 1.0)))

    if source not in G:
        return {"error": f"Source {source} not in topology"}

    # Run step-by-step recording
    visited = set()
    distances = {n: float("inf") for n in nodes}
    previous = {n: None for n in nodes}
    distances[source] = 0.0

    steps = []

    while len(visited) < len(nodes):
        # Pick unvisited node with min distance
        unvisited = {n: distances[n] for n in nodes if n not in visited}
        if not unvisited or min(unvisited.values()) == float("inf"):
            break
        current_node = min(unvisited, key=unvisited.get)
        current_dist = distances[current_node]
        visited.add(current_node)

        step_record = {
            "step": len(steps) + 1,
            "selected_node": current_node,
            "current_distance": current_dist,
            "visited_nodes": list(visited),
            "updated_neighbors": [],
            "distance_table_snapshot": dict(distances)
        }

        # Check neighbors
        for neighbor in G.neighbors(current_node):
            if neighbor not in visited:
                weight = G[current_node][neighbor]["weight"]
                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current_node
                    step_record["updated_neighbors"].append({
                        "neighbor": neighbor,
                        "old_distance": step_record["distance_table_snapshot"][neighbor],
                        "new_distance": new_dist,
                        "via": current_node
                    })

        steps.append(step_record)

    # Build routing table for source
    routing_table = []
    for dst in nodes:
        if dst == source:
            continue
        dist = distances[dst]
        if dist < float("inf"):
            # backtrack to find first hop
            curr = dst
            path = [curr]
            while previous[curr] and previous[curr] != source:
                curr = previous[curr]
                path.append(curr)
            first_hop = curr
            path.append(source)
            path.reverse()
            routing_table.append({
                "destination": dst,
                "cost": dist,
                "next_hop": first_hop,
                "full_path": path
            })
        else:
            routing_table.append({
                "destination": dst,
                "cost": "UNREACHABLE",
                "next_hop": None,
                "full_path": []
            })

    return {
        "algorithm": "Dijkstra Link-State Algorithm",
        "source": source,
        "steps": steps,
        "final_distances": distances,
        "routing_table": routing_table
    }


def calculate_distance_vector(nodes: List[str], links: List[Dict[str, Any]], iterations: int = 4) -> Dict[str, Any]:
    """
    Simulates Distance Vector (Bellman-Ford / RIP) periodic routing updates.
    """
    # Direct cost matrix
    costs = {n: {m: float("inf") for m in nodes} for n in nodes}
    for n in nodes:
        costs[n][n] = 0.0
    for l in links:
        s, t = l["source"], l["target"]
        w = float(l.get("cost", 1.0))
        costs[s][t] = w
        costs[t][s] = w

    # Routing tables: table[node][dest] = {"cost": c, "next_hop": h}
    tables = {}
    for n in nodes:
        tables[n] = {}
        for d in nodes:
            if n == d:
                tables[n][d] = {"cost": 0.0, "next_hop": n}
            elif costs[n][d] < float("inf"):
                tables[n][d] = {"cost": costs[n][d], "next_hop": d}
            else:
                tables[n][d] = {"cost": float("inf"), "next_hop": None}

    history = [{
        "iteration": 0,
        "description": "Initial state: each router knows only direct neighbor costs",
        "tables": {n: {d: dict(tables[n][d]) for d in nodes} for n in nodes}
    }]

    # Run iterations
    for it in range(1, iterations + 1):
        changed = False
        new_tables = {n: {d: dict(tables[n][d]) for d in nodes} for n in nodes}

        for i in nodes:
            for j in nodes:
                if i == j:
                    continue
                # Bellman-Ford equation: D_i(j) = min_v { c(i, v) + D_v(j) }
                for v in nodes:
                    if costs[i][v] < float("inf") and v != i:
                        via_cost = costs[i][v] + tables[v][j]["cost"]
                        if via_cost < new_tables[i][j]["cost"]:
                            new_tables[i][j]["cost"] = via_cost
                            new_tables[i][j]["next_hop"] = v
                            changed = True

        tables = new_tables
        history.append({
            "iteration": it,
            "description": f"Iteration {it}: Exchange distance vectors with direct neighbors",
            "changed": changed,
            "tables": {n: {d: dict(tables[n][d]) for d in nodes} for n in nodes}
        })
        if not changed:
            break

    return {
        "algorithm": "Distance Vector (Bellman-Ford)",
        "iterations_run": len(history) - 1,
        "converged": not changed,
        "history": history
    }

