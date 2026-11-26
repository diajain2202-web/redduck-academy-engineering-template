// 01-common-sense-check/src/Checkout.cs
// A minimal order service. Fix the flaw. Plain C#, no framework.
using System.Collections.Generic;

public record CatalogEntry(string Name, int Price); // price in cents
public record OrderItem(string ProductId, int Quantity, int Price);
public record OrderRequestItem(string ProductId, int Quantity);
public record OrderRequest(List<OrderRequestItem> Items);
public record Order(string Id, List<OrderItem> Items, int Total);

public static class Checkout
{
    // Product catalog.
    public static readonly Dictionary<string, CatalogEntry> Catalog = new()
    {
        ["sku-blue-tshirt"] = new CatalogEntry("Blue T-shirt", 2000),
        ["sku-red-mug"] = new CatalogEntry("Red mug", 900),
    };

    static readonly List<Order> Orders = new();

    // Create an order from a request, store it, and return it.
    public static Order CreateOrder(string id, OrderRequest request)
    {
        int total = 0;
        var items = new List<OrderItem>();
        foreach (var requestedItem in request.Items)
        {
            if (!Catalog.TryGetValue(requestedItem.ProductId, out var catalogEntry))
            {
                throw new ArgumentException($"Unknown product: {requestedItem.ProductId}");
            }

            if (requestedItem.Quantity <= 0)
            {
                throw new ArgumentOutOfRangeException(nameof(requestedItem.Quantity), "Quantity must be positive");
            }

            var item = new OrderItem(requestedItem.ProductId, requestedItem.Quantity, catalogEntry.Price);
            items.Add(item);
            total = checked(total + checked(item.Quantity * item.Price));
        }
        var order = new Order(id, items, total);
        Orders.Add(order);
        return order;
    }

    // Look up a stored order by its id.
    public static Order? GetOrder(string id)
    {
        foreach (var order in Orders)
        {
            if (order.Id == id)
            {
                return order;
            }
        }
        return null;
    }
}
