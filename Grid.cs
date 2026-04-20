using UnityEngine;
using CodeMonkey.Utils;

public class Grid
{
    private int width;
    private int height;
    private float cellSize;
    private Vector3 originPosition;
    private int [,] gridArray;
    private TextMesh[,] debugTextArray;
    
    public const int CELL_EMPTY = 0;
    public const int CELL_BLOCKED = -1;
    public const int CELL_OCCUPIED = 1;

    public Grid(int width, int height, float cellSize, Vector3 originPosition, float obstacleProbability = 0.2f) {
        this.width = width;
        this.height = height;
        this.cellSize = cellSize;
        this.originPosition = originPosition;

        gridArray = new int[width, height];
        debugTextArray = new TextMesh[width, height];

        GenerateRandomObstacles(obstacleProbability);

        Debug.Log(width + ", " + height);

        for (int x = 0; x < gridArray.GetLength(0); x++) {
            for (int y = 0; y < gridArray.GetLength(1); y++) {
                string cellText = GetCellText(gridArray[x, y]);
                Color textColor = GetCellColor(gridArray[x, y]);
                
                debugTextArray[x, y] = UtilsClass.CreateWorldText(
                    cellText, 
                    null, 
                    GetWorldPosition(x, y) + new Vector3(cellSize, cellSize) * .5f, 
                    20, 
                    textColor, 
                    TextAnchor.MiddleCenter
                );
                
                Debug.DrawLine(GetWorldPosition(x, y), GetWorldPosition(x, y + 1), Color.white, 100f);
                Debug.DrawLine(GetWorldPosition(x, y), GetWorldPosition(x + 1, y), Color.white, 100f);
            }
        }
        
        Debug.DrawLine(GetWorldPosition(0, height), GetWorldPosition(width, height), Color.white, 100f);
        Debug.DrawLine(GetWorldPosition(width, 0), GetWorldPosition(width, height), Color.white, 100f);
    }

    private void GenerateRandomObstacles(float probability) {
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                if (Random.value < probability) {
                    gridArray[x, y] = CELL_BLOCKED;
                } else {
                    gridArray[x, y] = CELL_EMPTY;
                }
            }
        }
    }

    private string GetCellText(int cellValue) {
        switch (cellValue) {
            case CELL_BLOCKED: return "X";
            case CELL_EMPTY: return "0";
            case CELL_OCCUPIED: return "1";
            default: return cellValue.ToString();
        }
    }

    private Color GetCellColor(int cellValue) {
        switch (cellValue) {
            case CELL_BLOCKED: return Color.red;
            case CELL_EMPTY: return Color.white;
            case CELL_OCCUPIED: return Color.green;
            default: return Color.white;
        }
    }

    // Публичный метод для получения мировых координат
    public Vector3 GetWorldPosition(int x, int y) {
        return new Vector3(x, y) * cellSize + originPosition;
    }

    // Публичный метод для преобразования мировых координат в координаты сетки
    public Vector2Int WorldToGridPosition(Vector3 worldPosition) {
        int x = Mathf.FloorToInt((worldPosition - originPosition).x / cellSize);
        int y = Mathf.FloorToInt((worldPosition - originPosition).y / cellSize);
        return new Vector2Int(x, y);
    }

    private void GetXY(Vector3 worldPosition, out int x, out int y) {
        x = Mathf.FloorToInt((worldPosition - originPosition).x / cellSize);
        y = Mathf.FloorToInt((worldPosition - originPosition).y / cellSize);
    }

    public void SetValue(int x, int y, int value) {
        if (x >= 0 && y >= 0 && x < width && y < height) {
            if (gridArray[x, y] != CELL_BLOCKED) {
                gridArray[x, y] = value;
                debugTextArray[x, y].text = GetCellText(value);
                debugTextArray[x, y].color = GetCellColor(value);
            } else {
                Debug.Log($"Клетка ({x}, {y}) является преградой и не может быть изменена!");
            }
        }
    }

    public void SetValue(Vector3 worldPosition, int value) {
        int x, y;
        GetXY(worldPosition, out x, out y);
        SetValue(x, y, value);
    }

    public int GetValue(int x, int y) {
        if (x >= 0 && y >= 0 && x < width && y < height) {
            return gridArray[x, y];
        } else {
            return CELL_EMPTY;
        }
    }
    
    public int GetValue(Vector3 worldPosition) {
        int x, y;
        GetXY(worldPosition, out x, out y);
        return GetValue(x, y);
    }
    
    public bool IsCellInteractable(int x, int y) {
        if (x >= 0 && y >= 0 && x < width && y < height) {
            return gridArray[x, y] != CELL_BLOCKED;
        }
        return false;
    }
    
    public bool IsCellInteractable(Vector3 worldPosition) {
        int x, y;
        GetXY(worldPosition, out x, out y);
        return IsCellInteractable(x, y);
    }
    
    public System.Collections.Generic.List<Vector2Int> GetObstaclePositions() {
        var obstacles = new System.Collections.Generic.List<Vector2Int>();
        
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                if (gridArray[x, y] == CELL_BLOCKED) {
                    obstacles.Add(new Vector2Int(x, y));
                }
            }
        }
        
        return obstacles;
    }
    
    // Методы для получения размеров сетки
    public int GetWidth() {
        return width;
    }
    
    public int GetHeight() {
        return height;
    }
    
    public float GetCellSize() {
        return cellSize;
    }
    
    public Vector3 GetOriginPosition() {
        return originPosition;
    }
    
    // Метод для получения всех свободных клеток
    public System.Collections.Generic.List<Vector2Int> GetEmptyCells() {
        var emptyCells = new System.Collections.Generic.List<Vector2Int>();
        
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                if (gridArray[x, y] == CELL_EMPTY) {
                    emptyCells.Add(new Vector2Int(x, y));
                }
            }
        }
        
        return emptyCells;
    }
    
    // Метод для проверки, пуста ли клетка
    public bool IsCellEmpty(int x, int y) {
        if (x >= 0 && y >= 0 && x < width && y < height) {
            return gridArray[x, y] == CELL_EMPTY;
        }
        return false;
    }
    
    // Метод для проверки, является ли клетка преградой
    public bool IsCellBlocked(int x, int y) {
        if (x >= 0 && y >= 0 && x < width && y < height) {
            return gridArray[x, y] == CELL_BLOCKED;
        }
        return false;
    }
    
    // Метод для проверки, занята ли клетка
    public bool IsCellOccupied(int x, int y) {
        if (x >= 0 && y >= 0 && x < width && y < height) {
            return gridArray[x, y] == CELL_OCCUPIED;
        }
        return false;
    }
    
    // Метод для очистки клетки (делает её пустой, если это не преграда)
    public void ClearCell(int x, int y) {
        if (x >= 0 && y >= 0 && x < width && y < height) {
            if (gridArray[x, y] != CELL_BLOCKED) {
                gridArray[x, y] = CELL_EMPTY;
                debugTextArray[x, y].text = GetCellText(CELL_EMPTY);
                debugTextArray[x, y].color = GetCellColor(CELL_EMPTY);
            }
        }
    }
}