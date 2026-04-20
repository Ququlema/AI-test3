using UnityEngine;
using System.Collections.Generic;

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
    
    public Vector3 GetWorldPosition(int x, int y)
    {
        if (grid == null || !IsWithinGrid(x, y)) 
            return Vector3.zero;
        return grid.GetWorldPosition(x, y);
    }
    
    public bool IsCellInteractable(int x, int y)
    {
        if (grid == null || !IsWithinGrid(x, y)) 
            return false;
        return grid.IsCellInteractable(x, y);
    }
    
    public void SetCellValue(int x, int y, int value)
    {
        if (grid != null && IsWithinGrid(x, y)) 
            grid.SetValue(x, y, value);
        else
            Debug.LogWarning($"Попытка установить значение за пределами сетки: ({x},{y})");
    }
    
    public int GetCellValue(int x, int y)
    {
        if (grid == null || !IsWithinGrid(x, y)) 
            return -1;
        return grid.GetValue(x, y);
    }
    
    void OnDrawGizmos()
    {
        if (!showGridGizmos) return;
        
        // Fallback для Editor Mode
        if (grid == null && Application.isPlaying)
            return;
        
        Gizmos.color = gridColor;
        
        // Рисуем линии сетки используя параметры, даже если grid == null
        int width = grid != null ? gridWidth : this.gridWidth;
        int height = grid != null ? gridHeight : this.gridHeight;
        Vector3 origin = grid != null ? originPosition : this.originPosition;
        float size = grid != null ? cellSize : this.cellSize;
        
        for (int x = 0; x <= width; x++)
        {
            Vector3 start = origin + new Vector3(x * size, 0, 0);
            Vector3 end = origin + new Vector3(x * size, height * size, 0);
            Gizmos.DrawLine(start, end);
        }
        
        for (int y = 0; y <= height; y++)
        {
            Vector3 start = origin + new Vector3(0, y * size, 0);
            Vector3 end = origin + new Vector3(width * size, y * size, 0);
            Gizmos.DrawLine(start, end);
        }
    }
    
    public Vector2Int GetGridSize() => new Vector2Int(gridWidth, gridHeight);
    public float GetCellSize() => cellSize;
    public Vector3 GetOriginPosition() => originPosition;
    
    public bool IsWithinGrid(int x, int y) => 
        x >= 0 && x < gridWidth && y >= 0 && y < gridHeight;
    
    public bool IsWithinGrid(Vector2Int gridPosition) => 
        IsWithinGrid(gridPosition.x, gridPosition.y);
    
    public void ClearOccupiedCells()
    {
        if (grid == null) 
        {
            Debug.LogWarning("Grid не инициализирован");
            return;
        }
        
        int clearedCount = 0;
        for (int x = 0; x < gridWidth; x++)
        {
            for (int y = 0; y < gridHeight; y++)
            {
                if (grid.GetValue(x, y) == Grid.CELL_OCCUPIED)
                {
                    grid.SetValue(x, y, Grid.CELL_EMPTY);
                    clearedCount++;
                }
            }
        }
        Debug.Log($"Очищено ячеек: {clearedCount}");
    }
    
    public Vector2Int GetRandomEmptyCell()
    {
        if (grid == null)
        {
            Debug.LogError("Grid не инициализирован");
            return new Vector2Int(-1, -1);
        }
        
        var emptyCells = GetAllEmptyCells();
        if (emptyCells.Count == 0)
        {
            Debug.LogWarning("Нет свободных клеток в сетке!");
            return new Vector2Int(-1, -1);
        }
        
        return emptyCells[Random.Range(0, emptyCells.Count)];
    }
    
    public List<Vector2Int> GetAllEmptyCells()
    {
        var emptyCells = new List<Vector2Int>();
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