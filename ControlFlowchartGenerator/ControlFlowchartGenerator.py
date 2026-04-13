import CfgBuilder

parsing_result = [
    {
        "id": 1,
        "type": "if_condition",
        "content": "x > 0",
        "next_if_true": 2,
        "next_if_false": 3
    },
    {
        "id": 2,
        "type": "statement",
        "content": "print('Positiv')",
        "next": 3
    },
    {
        "id": 3,
        "type": "end",
        "content": "Ende"
    }
]

if __name__ == "__main__":
    cfgBuilder = CfgBuilder.CfgBuilder()
    graph = cfgBuilder.createGraph(parsing_result)