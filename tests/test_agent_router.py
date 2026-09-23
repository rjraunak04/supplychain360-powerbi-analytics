from agent.router import route_question

def test_inventory_route():
    assert route_question("Which SKUs are understocked and need reorder?") == "inventory"

def test_procurement_route():
    assert route_question("Which supplier has purchase receipt issues?") == "procurement"

def test_fulfillment_route():
    assert route_question("Why are backorders increasing?") == "fulfillment"

def test_sales_route():
    assert route_question("Show revenue and profit demand trend") == "sales"

def test_unknown_route():
    assert route_question("hello there") == "general"
