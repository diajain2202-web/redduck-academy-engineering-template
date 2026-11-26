// 01-common-sense-check/src/Checkout.java
// A minimal order service. Fix the flaw. Plain Java, no framework.
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class Checkout {
    record CatalogEntry(String name, int price) {} // price in cents
    record OrderItem(String productId, int quantity, int price) {}
    record OrderRequestItem(String productId, int quantity) {}
    record OrderRequest(List<OrderRequestItem> items) {}
    record Order(String id, List<OrderItem> items, int total) {}

    // Product catalog.
    static final Map<String, CatalogEntry> CATALOG = Map.of(
        "sku-blue-tshirt", new CatalogEntry("Blue T-shirt", 2000),
        "sku-red-mug", new CatalogEntry("Red mug", 900)
    );

    static final List<Order> ORDERS = new ArrayList<>();

    // Create an order from a request, store it, and return it.
    static Order createOrder(String id, OrderRequest request) {
        int total = 0;
        List<OrderItem> items = new ArrayList<>();
        for (OrderRequestItem requestedItem : request.items()) {
            CatalogEntry catalogEntry = CATALOG.get(requestedItem.productId());
            if (catalogEntry == null) {
                throw new IllegalArgumentException("Unknown product: " + requestedItem.productId());
            }

            if (requestedItem.quantity() <= 0) {
                throw new IllegalArgumentException("Quantity must be positive");
            }

            OrderItem item = new OrderItem(
                requestedItem.productId(), requestedItem.quantity(), catalogEntry.price()
            );
            items.add(item);
            total = Math.addExact(total, Math.multiplyExact(item.quantity(), item.price()));
        }
        Order order = new Order(id, items, total);
        ORDERS.add(order);
        return order;
    }

    // Look up a stored order by its id.
    static Order getOrder(String id) {
        for (Order order : ORDERS) {
            if (order.id().equals(id)) {
                return order;
            }
        }
        return null;
    }
}
