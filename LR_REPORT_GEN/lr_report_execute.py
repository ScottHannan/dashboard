from lr_report_init import application
import lr_comparison_tab

###################################
#      MADE BY SCOTT HANNAN       #
#        AUGUST 20th 2019         #
#  Take Loadrunner summaries and  #
#  query them turning them into   #
#  nice tables and graphs         #
#  Requires python3               #
###################################

#### THIS IS THE EXECUTABLE FILE THIS IS WHAT IS CALLED TO START THE DASHBOARD ####
## This is in a seperate file so we do not have circular imports which would cause a
## dead lock in the app execution

if __name__ == '__main__':
  application.run()
