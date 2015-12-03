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
        # right_goal = self.get_goal_right()
        # left_goal = self.get_goal_left()
        # return  right_goal * math.copysign(right_goal,1) < right * math.copysign(right_goal,1) and \
        #         left_goal * math.copysign(left_goal,1) < left * math.copysign(left_goal,1)
        return self.get_goal_right() < right and self.get_goal_left() < left
