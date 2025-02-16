"""
class TreeModel : public QAbstractItemModel
{
    Q_OBJECT

public:
    Q_DISABLE_COPY_MOVE(TreeModel)

    explicit TreeModel(const QString &data, QObject *parent = nullptr);
    ~TreeModel() override;

    QVariant data(const QModelIndex &index, int role) const override;
    Qt::ItemFlags flags(const QModelIndex &index) const override;
    QVariant headerData(int section, Qt::Orientation orientation,
                        int role = Qt::DisplayRole) const override;
    QModelIndex index(int row, int column,
                      const QModelIndex &parent = {}) const override;
    QModelIndex parent(const QModelIndex &index) const override;
    int rowCount(const QModelIndex &parent = {}) const override;
    int columnCount(const QModelIndex &parent = {}) const override;

private:
    static void setupModelData(const QList<QStringView> &lines, TreeItem *parent);

    std::unique_ptr<TreeItem> rootItem;
};

TreeModel::TreeModel(const QString &data, QObject *parent)
    : QAbstractItemModel(parent)
    , rootItem(std::make_unique<TreeItem>(QVariantList{tr("Title"), tr("Summary")}))
{
    setupModelData(QStringView{data}.split(u'\n'), rootItem.get());
}

TreeModel::~TreeModel() = default;

QModelIndex TreeModel::index(int row, int column, const QModelIndex &parent) const
{
    if (!hasIndex(row, column, parent))
        return {};

    TreeItem *parentItem = parent.isValid()
        ? static_cast<TreeItem*>(parent.internalPointer())
        : rootItem.get();

    if (auto *childItem = parentItem->child(row))
        return createIndex(row, column, childItem);
    return {};
}

QModelIndex TreeModel::parent(const QModelIndex &index) const
{
    if (!index.isValid())
        return {};

    auto *childItem = static_cast<TreeItem*>(index.internalPointer());
    TreeItem *parentItem = childItem->parentItem();

    return parentItem != rootItem.get()
        ? createIndex(parentItem->row(), 0, parentItem) : QModelIndex{};
}

int TreeModel::rowCount(const QModelIndex &parent) const
{
    if (parent.column() > 0)
        return 0;

    const TreeItem *parentItem = parent.isValid()
        ? static_cast<const TreeItem*>(parent.internalPointer())
        : rootItem.get();

    return parentItem->childCount();
}

int TreeModel::columnCount(const QModelIndex &parent) const
{
    if (parent.isValid())
        return static_cast<TreeItem*>(parent.internalPointer())->columnCount();
    return rootItem->columnCount();
}

QVariant TreeModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || role != Qt::DisplayRole)
        return {};

    const auto *item = static_cast<const TreeItem*>(index.internalPointer());
    return item->data(index.column());
}

Qt::ItemFlags TreeModel::flags(const QModelIndex &index) const
{
    return index.isValid()
        ? QAbstractItemModel::flags(index) : Qt::ItemFlags(Qt::NoItemFlags);
}

QVariant TreeModel::headerData(int section, Qt::Orientation orientation,
                               int role) const
{
    return orientation == Qt::Horizontal && role == Qt::DisplayRole
        ? rootItem->data(section) : QVariant{};

}
"""

from typing import Any, Optional, Mapping

from PySide6.QtCore import Qt, QAbstractItemModel, QModelIndex

from tree_item import TreeItem


def setup_model_data(items: list[Mapping[str, Any]], root: TreeItem) -> None:
    for it in items:
        root.append_child(TreeItem(it, root))


class TreeModel(QAbstractItemModel):
    def __init__(
        self, items: list[Mapping[str, Any]], /, parent: Optional[Any] = None
    ) -> None:
        super().__init__(parent)
        self.root_item = TreeItem()
        setup_model_data(items, self.root_item)

    def index(self, row: int, column: int, parent: Any = None) -> Any:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        parent_item = parent.internalPointer() if parent.isValid() else self.root_item

        if child_item := parent_item.child(row):
            return self.createIndex(row, column, child_item)
        return QModelIndex()

    def parent(self, index: QModelIndex) -> Any:
        if not index.isValid():
            return QModelIndex()

        child_item = index.internalPointer()
        parent_item = child_item.parent_item()

        if parent_item is self.root_item:
            return QModelIndex()
        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent: Any = None) -> int:
        if parent.column() > 0:
            return 0

        parent_item = parent.internalPointer() if parent.isValid() else self.root_item
        return parent_item.child_count()

    def columnCount(self, parent: Any = None) -> int:
        if parent.isValid():
            return parent.internalPointer().column_count()
        return self.root_item.column_count()

    def data(self, index: QModelIndex, role: int) -> Any:
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            item = index.internalPointer()
            return item.data(index.column())

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        if index.isValid():
            return QAbstractItemModel.flags(self, index)
        return Qt.ItemFlag.NoItemFlags

    def headerData(self, section: int, orientation: Qt.Orientation, role: int) -> Any:
        if (
            orientation == Qt.Orientation.Horizontal
            and role == Qt.ItemDataRole.DisplayRole
        ):
            return ["Title", "Description"][section]
