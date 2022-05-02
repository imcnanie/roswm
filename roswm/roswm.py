# ['PARAM_REL_TOL', '_Node__clients', '_Node__executor_weakref', '_Node__guards', '_Node__handle', '_Node__publishers', '_Node__services', '_Node__subscriptions', '_Node__timers', '_Node__waitables', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_allow_undeclared_parameters', '_apply_descriptor', '_apply_descriptor_and_set', '_apply_descriptors', '_apply_floating_point_range', '_apply_integer_range', '_check_undeclared_parameters', '_clock', '_context', '_count_publishers_or_subscribers', '_default_callback_group', '_descriptors', '_get_info_by_topic', '_logger', '_parameter_event_publisher', '_parameter_overrides', '_parameter_service', '_parameters', '_parameters_callbacks', '_rate_group', '_set_parameters', '_set_parameters_atomically', '_time_source', '_validate_qos_or_depth_parameter', '_validate_topic_or_service_name', '_wake_executor', 'add_on_set_parameters_callback', 'add_waitable', 'clients', 'context', 'count_publishers', 'count_subscribers', 'create_client', 'create_guard_condition', 'create_publisher', 'create_rate', 'create_service', 'create_subscription', 'create_timer', 'declare_parameter', 'declare_parameters', 'default_callback_group', 'describe_parameter', 'describe_parameters', 'destroy_client', 'destroy_guard_condition', 'destroy_node', 'destroy_publisher', 'destroy_rate', 'destroy_service', 'destroy_subscription', 'destroy_timer', 'executor', 'get_client_names_and_types_by_node', 'get_clock', 'get_logger', 'get_name', 'get_namespace', 'get_node_names', 'get_node_names_and_namespaces', 'get_node_names_and_namespaces_with_enclaves', 'get_parameter', 'get_parameter_or', 'get_parameters', 'get_parameters_by_prefix', 'get_publisher_names_and_types_by_node', 'get_publishers_info_by_topic', 'get_service_names_and_types', 'get_service_names_and_types_by_node', 'get_subscriber_names_and_types_by_node', 'get_subscriptions_info_by_topic', 'get_topic_names_and_types', 'guards', 'handle', 'has_parameter', 'publishers', 'remove_on_set_parameters_callback', 'remove_waitable', 'services', 'set_descriptor', 'set_parameters', 'set_parameters_atomically', 'set_parameters_callback', 'subscriptions', 'timers', 'undeclare_parameter', 'waitables'
        
# BAD ACESS ERRORS: DISPLAY=:1 !!!!

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

from Xlib.display import Display
from Xlib import X, XK

from subprocess import Popen
import psutil
import os

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 30)
        timer_period = 0.001  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

        self.init_x()

    def timer_callback(self):
        #pass
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        #self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1
        self.x_loop()

    def init_x(self):

        #node_dummy = Node("_ros2cli_dummy_to_show_topic_list")

        #print(dir(node_dummy))
        #[print(x) for x in self.get_node_names_and_namespaces()]
        #self.topic_list = node_dummy.get_topic_names_and_types()
        #node_dummy.destroy_node()
        
        #'pub':'subs'
        self.rosNodes = {
        }
        
        self.display = Display()
        self.screen = self.display.screen()
        self.root = self.screen.root

        self.root.grab_key(self.display.keysym_to_keycode(XK.string_to_keysym("F1")),
                      X.Mod1Mask,
                      1,
                      X.GrabModeAsync,
                      X.GrabModeAsync)

        # reload ROS nodes
        self.root.grab_key(self.display.keysym_to_keycode(XK.string_to_keysym("R")),
                      X.Mod1Mask,
                      1,
                      X.GrabModeAsync,
                      X.GrabModeAsync)
        
        self.root.grab_key(self.display.keysym_to_keycode(XK.string_to_keysym("Return")),
                      X.Mod1Mask,
                      1,
                      X.GrabModeAsync,
                      X.GrabModeAsync)
       
        self.root.grab_button(1,
                         X.Mod1Mask,
                         1,
                         X.ButtonPressMask|X.ButtonReleaseMask|X.PointerMotionMask,
                         X.GrabModeAsync,
                         X.GrabModeAsync,
                         X.NONE,
                         X.NONE)
       
        self.root.grab_button(3,
                         X.Mod1Mask,
                         1,
                         X.ButtonPressMask|X.ButtonReleaseMask|X.PointerMotionMask,
                         X.GrabModeAsync,
                         X.GrabModeAsync,
                         X.NONE,
                         X.NONE)
       
        self.start = None
        self.attr = None
       
        background_color = "lightgreen"
        #os.system('xsetroot -solid "' + background_color + '"')
        #xcol_string = '\e]11;rgb:aa/ff/dd\a'
        xcol_string = "echo -e \'\e]11;rgb:11/00/00\\a\'"
        #os.system("./col.sh aa bb cc")
        commands = ['xsetroot -solid "' + background_color + '"']
        #            "./col.sh ee ff cc"]
        processes = [Popen(cmd, shell=True) for cmd in commands]
        #print("xterm -hold -e \'"+xcol_string)

        self.root.change_attributes(event_mask=X.ExposureMask)  # "adds" this event mask
        self.gc_bg = self.root.create_gc(foreground = self.screen.white_pixel,
                               background = self.screen.black_pixel)
        self.gc = self.root.create_gc(foreground = self.screen.black_pixel,
                            background = self.screen.white_pixel)
        '''gc = root.create_gc(
            line_width = 4,
            line_style = X.LineOnOffDash,
            fill_style = X.FillOpaqueStippled,
            fill_rule  = X.WindingRule,
            cap_style  = X.CapButt,
            join_style = X.JoinMiter,
            foreground = screen.white_pixel,
            background = screen.black_pixel,
            function = X.GXxor, 
            graphics_exposures = False,
            subwindow_mode = X.IncludeInferiors,
            )  
        '''

       
        #test = root.poly_line(gc,
        #               X.CoordModeOrigin,
        #               [(0,0),(100,100)])
       
        #display.flush()
       

    def x_loop(self):
        ev = self.display.next_event()
        windows = self.root.query_tree().children
        #print(windows)
        #cords = w.get_geometry()['x'],w.get_geometry()['y']]
        
        if ev.type == X.KeyPress and ev.child != X.NONE:
            ev.child.configure(stack_mode = X.Above)
        elif ev.type == X.ButtonPress and ev.child != X.NONE:
            self.attr = ev.child.get_geometry()
            self.start = ev
        elif ev.type == X.MotionNotify and self.start:
            #XFillRectangle(display, window, DefaultGC(display, s), 20, 20, 10, 10)<
            
            self.root.clear_area(x = 0, y = 0,
                            width = self.root.get_geometry().width,
                            height = self.root.get_geometry().height,
                            exposures = True, onerror = None)
            xdiff = ev.root_x - self.start.root_x
            ydiff = ev.root_y - self.start.root_y
            self.start.child.configure(
                x = self.attr.x + (self.start.detail == 1 and xdiff or 0),
                y = self.attr.y + (self.start.detail == 1 and ydiff or 0),
                width = max(1, self.attr.width + (self.start.detail == 3 and xdiff or 0)),
                height = max(1, self.attr.height + (self.start.detail == 3 and ydiff or 0)))
            
            #root.clear_area(0,1000,1000)
            #root.fill_rectangle(gc_bg, 0, 0, root.get_geometry().width, root.get_geometry().height)
            #print()

            
            for n in self.get_node_names_and_namespaces():
                #print(n)
                if n[0].split('_')[-1].isnumeric() and n[0].split('_')[-1] != '0':
                    self.rosNodes[n[0]] = []
                    for x in self.get_publisher_names_and_types_by_node(n[0],n[1]):
                        if x[0] != '/parameter_events' and x[0] != '/rosout':
                            tops = []
                            for y in self.get_subscriptions_info_by_topic(x[0]):
                                winz = None
                                for x in range(len(windows)):
                                    w = windows[x]
                                    pid = w.get_full_property(self.display.intern_atom('_NET_WM_PID'), X.AnyPropertyType)
                                    if 'value' in dir(pid):
                                        if pid.value[0] == int(y.node_name.split("_")[-1]):
                                            winz = w # Your loops make me sick!
                                tops.append([y.node_name, winz])
                            
                            self.rosNodes[n[0]].append(tops) # xwindow ID, ROSPID
                                        

            window_lines = {}
            
            for x in range(len(windows)):
                w = windows[x]
                title = w.get_wm_class()
                pid = w.get_full_property(self.display.intern_atom('_NET_WM_PID'), X.AnyPropertyType)
                p = None
                ppid = None
                #if 'value' in dir(pid):
                #    p = psutil.Process(6390)
                #    ppid = p.ppid()
                #    p = psutil.Process(ppid)
                #    ppid = p.ppid()
                ptsd = None
                if 'value' in dir(pid):
                    for rp in self.rosNodes:
                        if str(pid.value[0]) in rp:
                            try:
                                ptsd = rp
                                ppid = [x[0] for x in self.rosNodes[rp][0]]
                                for ww in self.rosNodes[rp][0]:
                                    #print(w, ww[1])
                                    self.root.poly_line(self.gc,
                                                        X.CoordModeOrigin,
                                                        [(w.get_geometry().x,
                                                          w.get_geometry().y),
                                                         (ww[1].get_geometry().x,
                                                          ww[1].get_geometry().y)])

                            except:
                                pass
                                #print("wow")
                                #pw = 
                                #sw = l[1]
                                
                            
                        # into the matrix

                        #p = psutil.Process(int(rp.split("_")[-1]))
                        #ppid = p.ppid()
                        #p = psutil.Process(ppid)
                        #ppid = p.ppid()
                        #p = psutil.Process(ppid)
                        #ppid1 = p.ppid()
                        #window_pids[pid.value[0]] = "rp"+str(ppid)

                        
                    #p = psutil.Process(pid.value[0])
                    #ppid = p.ppid()
                    #print(ppid)

                #print(self.topic_list)
                if title is not None:
                    self.root.draw_text(self.gc,
                                        w.get_geometry().x-10,
                                        w.get_geometry().y-10,
                                        bytes(w.get_wm_class()[0]+" "+str(ptsd)+" "+str(ppid), 'utf-8'))  # changed the coords more towards the center
                                   #bytes(w.get_wm_class()[0]+" "+str(pid.value[0])+" "+str(ppid), 'utf-8'))  # changed the coords more towards the center

            #print(window_lines)
            self.display.flush()
            self.display.sync()
            
            
        elif ev.type == X.Expose:
            pass
        
        elif ev.type == X.ButtonRelease:
            self.start = None
            
            
        
            #root.poly_line(gc,
            #               X.CoordModeOrigin,
            #               [(0,0),(windows[0],windows[0])])
            #
            #display.flush()
    def xterm_color_string(self,r,g,b):
        return "echo -e \'e]11;rgb:"+r+"/"+g+"/"+b+"\a\'"


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    #rclpy.spin(minimal_publisher)
    while rclpy.ok():
        rclpy.spin_once(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
