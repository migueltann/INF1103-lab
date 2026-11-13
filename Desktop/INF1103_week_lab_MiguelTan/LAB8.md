# INF1103 Lab 8

## Predictions before running the tests

1. Deleting the local supplier variable leaves both products able to display the supplier because both retain a reference.
2. Removing the product from Inventory A leaves the product usable because the inventory only drops its reference. Inventory B can accept the same object.
3. Adding one product to two orders creates two distinct order lines that refer to one shared product.
4. The physical product prints `This product requires physical shipping.` The digital product prints `This product is delivered digitally.`

The observed results for all four predictions matched. See [the Word notes](lab8/INF1103_Lab8_Predict_First.docx) for details.

## Design review

[Open the UML class diagram](lab8/class-diagram.svg). The supplier reference is an association. Inventory aggregates products, which can exist in zero or more inventories in this implementation. Order creates its own lines and exposes them through a read-only tuple. A line refers to a product that can outlive the line.

Both Product subclasses inherit `update_stock(quantity)`, which sets the stock to the supplied quantity. A DigitalProduct override that raises `NotImplementedError` for valid quantities would violate LSP because callers rely on that operation for every Product. Keep the inherited method so digital stock continues to represent available units.

The same `show_product_details(product)` function calls `display_information()` and `get_fulfilment_info()` for both subclasses. Python selects the subclass implementation, and both subclasses preserve the Product method contract.

For the AI-assisted UML review, the plain association for Supplier and Product was accepted. The Inventory end of the aggregation was adjusted to `0..*` because the same Product reference can be shared by multiple inventories.

## Run and verify

Use Python 3.11 or later. The Dockerfile uses Python 3.12.

```bash
python3 main.py
python3 -m unittest discover -v
```

Options 7 and 8 remove a product and price an order. Order pricing uses the inventory's products and leaves stock counts as they were. The order exists for the current pricing interaction. Inventory save and load support existing Lab 7 records and store supplier details for Lab 8 records.

From this directory on a Docker-enabled machine, run the following commands for the submission screenshot.

```bash
git status --short --branch
git log -4 --oneline
docker build -f dockerfile -t inf1103-lab8 .
docker run --rm inf1103-lab8 python -m unittest discover -v
printf '1\n6\n' | docker run --rm -i inf1103-lab8
```
