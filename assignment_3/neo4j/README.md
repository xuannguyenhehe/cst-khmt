* Step 1: RUN DOCKER
Fisrtly, you must run Docker for Neo4j

```
    docker run -it --rm \
    --publish=7474:7474 --publish=7687:7687 \
    -e NEO4J_AUTH=none \
    --env NEO4JLABS_PLUGINS='["graph-data-science"]' \
    neo4j:4.4
```

Then, you access url with localhost:7474. Next, you log in without username or password.

* Step 2: LOAD NODES on Neo4j

```
    LOAD CSV WITH HEADERS
    FROM "https://docs.google.com/spreadsheets/d/e/2PACX-1vQksiimLamDT3dIbyhwalRoGGMKWvLQEjpp-ZtaZ_yLkBJYthIgM5VFJPAuJ1_kgm2wkkpH9-WQaEug/pub?output=csv"
    AS csvLine
    CREATE (a:Artist {id: csvLine.st_id, name: csvLine.st_name, genre1: csvLine.st_genre1, genre2: csvLine.st_genre2, genre3: csvLine.st_genre3,  genre4: csvLine.st_genre4, popularity: csvLine.popularity, followers: csvLine.followers})
```

* Step 3: LOAD EDGES on Neo4j

```
    :auto LOAD CSV WITH HEADERS from "https://docs.google.com/spreadsheets/d/e/2PACX-1vRCF7yi64R7NurFIwAFuY6eNiBGiG2nVpMfZ_uSUVleu5TLnKaIhfHaPSXMZxdC6_p7WMgnPRDjxxoi/pub?output=csv" AS csvLine
    CALL {
    WITH csvLine
    MATCH (a1:Artist {id: csvLine.st_id_x}), (a2:Artist {id: csvLine.st_id_y})
    CREATE (a1)-[:RELATE_TO {weight: 1}]->(a2)
    } IN TRANSACTIONS OF 500 ROWS
```

* Step 4: Set unweight for all edges

```
    CALL gds.graph.project(
        'exGraph',
        'Artist',
        {
            RELATE_TO: {
                orientation: 'UNDIRECTED'
            }
        },
        {
            relationshipProperties: 'weight'
        }
    )
```

* Step 5: RUN LOUVAIN algorithm

```
    CALL gds.louvain.stats('exGraph', { 
        tolerance: 0.00000000000000001
    })
    YIELD communityCount, modularity, modularities
```

* Step 6: RUN LEIDEN algorithm

```
    CALL gds.alpha.leiden.stats('exGraph', { 
    tolerance: 0.00000000000000001
    })
    YIELD communityCount, modularity, modularities
```