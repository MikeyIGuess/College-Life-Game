def draw(self, screen, player, time_manager, game):
        # ... existing code ...
        
        # Canvas notifications
        today_assignments, today_lectures = game.canvas.get_due_today()
        if today_assignments or today_lectures:
            font = pygame.font.Font(None, 24)
            notification = font.render(f"DUE TODAY: {len(today_assignments)} assignments, {len(today_lectures)} lectures", True, RED)
            screen.blit(notification, (20, WINDOW_HEIGHT - 60))