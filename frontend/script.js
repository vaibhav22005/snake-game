const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const gridSize = 15;
const tileSize = canvas.width / gridSize;

let snake;
let food;
let direction;
let nextDirection;
let score = 0;
let gameRunning = true;
let gameLoop;

function startGame() {

    snake = [
        { x: 7, y: 7 },
        { x: 6, y: 7 },
        { x: 5, y: 7 }
    ];

    direction = { x: 1, y: 0 };
    nextDirection = { x: 1, y: 0 };

    score = 0;
    gameRunning = true;

    document.getElementById("score").textContent = score;

    generateFood();

    clearInterval(gameLoop);
    gameLoop = setInterval(updateGame, 120);
}

function updateGame() {

    if (!gameRunning) return;

    direction = nextDirection;

    const head = {
        x: snake[0].x + direction.x,
        y: snake[0].y + direction.y
    };

    // Wall collision
    if (
        head.x < 0 ||
        head.x >= gridSize ||
        head.y < 0 ||
        head.y >= gridSize
    ) {
        gameOver();
        return;
    }

    // Snake collision
    for (let part of snake) {
        if (head.x === part.x && head.y === part.y) {
            gameOver();
            return;
        }
    }

    snake.unshift(head);

    // Food collision
    if (head.x === food.x && head.y === food.y) {

        score += 10;

        document.getElementById("score").textContent = score;

        generateFood();

    } else {
        snake.pop();
    }

    draw();
}

function draw() {

    // Background
    ctx.fillStyle = "#020617";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Food
    ctx.fillStyle = "#ef4444";

    ctx.beginPath();

    ctx.arc(
        food.x * tileSize + tileSize / 2,
        food.y * tileSize + tileSize / 2,
        tileSize / 3,
        0,
        Math.PI * 2
    );

    ctx.fill();

    // Snake
    snake.forEach((part, index) => {

        ctx.fillStyle =
            index === 0 ? "#4ade80" : "#22c55e";

        ctx.fillRect(
            part.x * tileSize + 1,
            part.y * tileSize + 1,
            tileSize - 2,
            tileSize - 2
        );
    });
}

function generateFood() {

    food = {
        x: Math.floor(Math.random() * gridSize),
        y: Math.floor(Math.random() * gridSize)
    };
}

function changeDirection(newDirection) {

    if (newDirection === "up" && direction.y !== 1) {
        nextDirection = { x: 0, y: -1 };
    }

    if (newDirection === "down" && direction.y !== -1) {
        nextDirection = { x: 0, y: 1 };
    }

    if (newDirection === "left" && direction.x !== 1) {
        nextDirection = { x: -1, y: 0 };
    }

    if (newDirection === "right" && direction.x !== -1) {
        nextDirection = { x: 1, y: 0 };
    }
}

document.addEventListener("keydown", function(event) {

    if (event.key === "ArrowUp" || event.key === "w") {
        changeDirection("up");
    }

    if (event.key === "ArrowDown" || event.key === "s") {
        changeDirection("down");
    }

    if (event.key === "ArrowLeft" || event.key === "a") {
        changeDirection("left");
    }

    if (event.key === "ArrowRight" || event.key === "d") {
        changeDirection("right");
    }
});

function gameOver() {

    gameRunning = false;

    clearInterval(gameLoop);

    alert("Game Over! Score: " + score);
}

function restartGame() {
    startGame();
    draw();
}

startGame();
