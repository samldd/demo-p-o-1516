__author__ = 'sam_l'

class drivingSession():

    def __init__(self,left,right):
        self.goal_left = left
        self.goal_right = right

    def get_goal_left(self):
        return self.goal_left

    def get_goal_right(self):
        return self.goal_right

    def goal_reached(self,left,right):
        return self.get_goal_right() < right and self.get_goal_left() < left
