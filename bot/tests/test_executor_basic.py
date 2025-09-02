from bot.core.executor import place_orders

def test_place_orders_returns_summary():
    summary = place_orders([{"symbol":"BTCUSDT","side":"BUY","size":100}], dry_run=True)
    assert summary["dry_run"] is True
    assert summary["placed"] == 1
    assert isinstance(summary["results"], list) and len(summary["results"]) == 1
    r0 = summary["results"][0]
    assert {"symbol","side","qty","price","order_id"}.issubset(set(r0.keys()))
