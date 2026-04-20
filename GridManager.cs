using UnityEngine;

public class GridManager : MonoBehaviour
{
    [Header("Настройки сетки")]
    [SerializeField] private int gridWidth = 10;
    [SerializeField] private int gridHeight = 10;
    [SerializeField] private float cellSize = 1f;
    [SerializeField] private Vector3 originPosition = Vector3.zero;
    [SerializeField] private float obstacleProbability = 0.2f;
    
    [Header("Визуализация")]
    [SerializeField] private bool showGridGizmos = true;
    [SerializeField] private Color gridColor = Color.white;
    
    private Grid grid;
    
    public Grid GetGrid() => grid;
    
    void Start()
    {
        CreateGrid();
    }
    
    public void CreateGrid()
    {
        grid = new Grid(gridWidth, gridHeight, cellSize, originPosition, obstacleProbability);
        Debug.Log($"Сетка создана: {gridWidth}x{gridHeight}");
    }
    
    public void CreateGrid(int width, int height, float cellSize, Vector3 origin)
    {
        gridWidth = width;
        gridHeight = height;
        this.cellSize = cellSize;
        originPosition = origin;
        CreateGrid();
    }
    
    // Методы-обертки для удобства
    public Vector3 GetWorldPosition(int x, int y)
    {
        return grid != null ? grid.GetWorldPosition(x, y) : Vector3.zero;
    }
    
    public bool IsCellInteractable(int x, int y)
    {
        return grid != null ? grid.IsCellInteractable(x, y) : false;
    }
    
    public void SetCellValue(int x, int y, int value)
    {
        if (grid != null) grid.SetValue(x, y, value);
    }
    
    public int GetCellValue(int x, int y)
    {
        return grid != null ? grid.GetValue(x, y) : 0;
    }
    
    void OnDrawGizmos()
    {
        if (!showGridGizmos || grid == null) return;
        
        Gizmos.color = gridColor;
        
        // Рисуем линии сетки
        for (int x = 0; x <= gridWidth; x++)
        {
            Vector3 start = originPosition + new Vector3(x * cellSize, 0, 0);
            Vector3 end = originPosition + new Vector3(x * cellSize, gridHeight * cellSize, 0);
            Gizmos.DrawLine(start, end);
        }
        
        for (int y = 0; y <= gridHeight; y++)
        {
            Vector3 start = originPosition + new Vector3(0, y * cellSize, 0);
            Vector3 end = originPosition + new Vector3(gridWidth * cellSize, y * cellSize, 0);
            Gizmos.DrawLine(start, end);
        }
    }
    
    // Дополнительные методы для удобства работы
    public Vector2Int GetGridSize()
    {
        return new Vector2Int(gridWidth, gridHeight);
    }
    
    public float GetCellSize()
    {
        return cellSize;
    }
    
    public Vector3 GetOriginPosition()
    {
        return originPosition;
    }
    
    // Проверка, находится ли позиция в пределах сетки
    public bool IsWithinGrid(int x, int y)
    {
        return x >= 0 && x < gridWidth && y >= 0 && y < gridHeight;
    }
    
    public bool IsWithinGrid(Vector2Int gridPosition)
    {
        return IsWithinGrid(gridPosition.x, gridPosition.y);
    }
    
    // Очистка сетки (удаление всех занятых клеток кроме препятствий)
    public void ClearOccupiedCells()
    {
        if (grid == null) return;
        
        for (int x = 0; x < gridWidth; x++)
        {
            for (int y = 0; y < gridHeight; y++)
            {
                if (grid.GetValue(x, y) == Grid.CELL_OCCUPIED)
                {
                    grid.SetValue(x, y, Grid.CELL_EMPTY);
                }
            }
        }
    }
    
    // Получение случайной свободной клетки
    public Vector2Int GetRandomEmptyCell()
    {
        if (grid == null) return Vector2Int.zero;
        
        Vector2Int randomCell;
        int attempts = 0;
        
        do
        {
            randomCell = new Vector2Int(
                Random.Range(0, gridWidth),
                Random.Range(0, gridHeight)
            );
            attempts++;
        }
        while (grid.GetValue(randomCell.x, randomCell.y) != Grid.CELL_EMPTY && attempts < 100);
        
        return randomCell;
    }
    
    // Получение всех свободных клеток
    public System.Collections.Generic.List<Vector2Int> GetAllEmptyCells()
    {
        var emptyCells = new System.Collections.Generic.List<Vector2Int>();
        
        if (grid == null) return emptyCells;
        
        for (int x = 0; x < gridWidth; x++)
        {
            for (int y = 0; y < gridHeight; y++)
            {
                if (grid.GetValue(x, y) == Grid.CELL_EMPTY)
                {
                    emptyCells.Add(new Vector2Int(x, y));
                }
            }
        }
        
        return emptyCells;
    }
}