"""
class TreeItem
{
public:
    explicit TreeItem(QVariantList data, TreeItem *parentItem = nullptr);

    void appendChild(std::unique_ptr<TreeItem> &&child);

    TreeItem *child(int row);
    int childCount() const;
    int columnCount() const;
    QVariant data(int column) const;
    int row() const;
    TreeItem *parentItem();

private:
    std::vector<std::unique_ptr<TreeItem>> m_childItems;
    QVariantList m_itemData;
    TreeItem *m_parentItem;
};

TreeItem::TreeItem(QVariantList data, TreeItem *parent)
    : m_itemData(std::move(data)), m_parentItem(parent)
{}

void TreeItem::appendChild(std::unique_ptr<TreeItem> &&child)
{
    m_childItems.push_back(std::move(child));
}

TreeItem *TreeItem::child(int row)
{
    return row >= 0 && row < childCount() ? m_childItems.at(row).get() : nullptr;
}

int TreeItem::childCount() const
{
    return int(m_childItems.size());
}

int TreeItem::row() const
{
    if (m_parentItem == nullptr)
        return 0;
    const auto it = std::find_if(m_parentItem->m_childItems.cbegin(), m_parentItem->m_childItems.cend(),
                                 [this](const std::unique_ptr<TreeItem> &treeItem) {
                                     return treeItem.get() == this;
                                 });

    if (it != m_parentItem->m_childItems.cend())
        return std::distance(m_parentItem->m_childItems.cbegin(), it);
    Q_ASSERT(false); // should not happen
    return -1;
}

int TreeItem::columnCount() const
{
    return int(m_itemData.count());
}

QVariant TreeItem::data(int column) const
{
    return m_itemData.value(column);
}

TreeItem *TreeItem::parentItem()
{
    return m_parentItem;
}
"""

from typing import Any, Mapping


class TreeItem:
    def __init__(
        self, data: Mapping[str, Any] = None, parent_item: "TreeItem" = None
    ) -> None:
        self.parent_item: "TreeItem" = parent_item
        self.item_data: list = []
        self.child_items: list["TreeItem"] = []

        if data is None:
            return

        self.item_data = [data["title"], data["description"]]

        if "items" in data:
            self.child_items: list["TreeItem"] = [
                TreeItem(it, self) for it in data["items"]
            ]

    def append_child(self, child: "TreeItem") -> None:
        self.child_items.append(child)

    def child(self, row: int) -> "TreeItem | None":
        if 0 <= row < self.child_count():
            return self.child_items[row]

    def child_count(self) -> int:
        return len(self.child_items)

    def row(self) -> int:
        return (
            0 if self.parent_item is None else self.parent_item.child_items.index(self)
        )

    def column_count(self) -> int:
        return len(self.item_data)

    def data(self, column: int) -> Any:
        if 0 <= column < self.column_count():
            return self.item_data[column]

    def parent(self) -> "TreeItem | None":
        return self.parent_item
