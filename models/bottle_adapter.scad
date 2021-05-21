$fn=60;
bottle_r = 53/2;

holder_thickness = 5;

servo_y = 12;
servo_x = 20;
servo_z = 40;


// servo insert test
//difference(){
//    
//    bottle_adapter();
//
//    translate([15,-50,0])
//    cube([50,100,100]);
//
//    translate([-80,-50,0])
//    cube([100,50,100]);
//
//    translate([-65,-50,0])
//    cube([50,100,100]);
//}

bottle_adapter();

module bottle_adapter(){
    adapter_h = 120;
    insert_padding = 0.1;
    butane_channel_r = 10;
    butane_channel_h = 20;
    
    flat_surface_width = 50;
    
    servo_rotor_depth = 20;
    cap_depth = 8;
    
    servo_cutout_r = 56/2;
    
    hook_insert = 10;
    
    lighter_assembly_servo = [servo_x+40, servo_y-2, servo_z+20];

    difference(){
        union(){
        hull(){
            // butane servo
            translate([0,
                       bottle_r + holder_thickness + insert_padding,
                       adapter_h/2
                     ])
            rotate([0,0,90])
            cube([holder_thickness,
                  flat_surface_width,
                  adapter_h],
                center=true);

            cylinder(r=bottle_r + holder_thickness, h=adapter_h/2);
        }
            translate([bottle_r -25,
               -bottle_r/3 - servo_y *1.88,
               0
             ]){
        difference(){
            cube(lighter_assembly_servo);
    
            translate([(lighter_assembly_servo[0])/2 + 15,
                        lighter_assembly_servo[1]/1.3,
                        lighter_assembly_servo[2]/6])
            servo_insert();
        }
    }
    }
        
        cylinder(r=bottle_r + insert_padding, h=200);
        
        // servo insert
        translate([0,
                   bottle_r + holder_thickness,
                   adapter_h - servo_z - 10
                 ])
        servo_insert();
        
        translate([0,
                   bottle_r-2,
                   adapter_h - servo_cutout_r+10])
        rotate([90,0,0])
        cylinder(r=servo_cutout_r, h=20);
        
        translate([0,0,hook_insert])
        cube([100, hook_insert,hook_insert],center=true);
    }
}

module servo_insert(){
    offset = 7;
    
    screw_r = 2/2;
    normal_screw_r = 4/2;
    z_offset = 2;
    
    insert_padding = 0.5;
    insert_thickess = 20;
    
    holder_spacing_from_center = 4 + normal_screw_r;
    
    translate([0,0,servo_z/2])
    cube([insert_thickess + insert_padding,
          insert_thickess + insert_padding,
          servo_z],center=true);
    
    // top holes
    color("gold")
    translate([-holder_spacing_from_center,
               0,
               servo_z + z_offset + normal_screw_r
             ])
    rotate([90,0,0])
    cylinder(r=screw_r, h=insert_thickess, center=true);
    
    color("red")
    translate([-holder_spacing_from_center,
               insert_thickess/4,
               servo_z + z_offset + normal_screw_r
             ])
    rotate([90,0,0])
    cylinder(r=normal_screw_r, h=insert_thickess/2, center=true);
    
    color("gold")
    translate([holder_spacing_from_center,
               0,
               servo_z + z_offset + normal_screw_r
             ])
    rotate([90,0,0])
    cylinder(r=screw_r, h=insert_thickess, center=true);
    
    color("red")
    translate([holder_spacing_from_center,
               insert_thickess/4,
               servo_z + z_offset + normal_screw_r
             ])
    rotate([90,0,0])
    cylinder(r=normal_screw_r, h=insert_thickess/2, center=true);
    
    // bottom holes
    color("gold")
    translate([-holder_spacing_from_center,
               0,
               -z_offset - normal_screw_r
             ])
    rotate([90,0,0])
    cylinder(r=screw_r, h=insert_thickess, center=true);
    
    color("red")
    translate([-holder_spacing_from_center,
               insert_thickess/4,
               -z_offset - normal_screw_r
             ])
    rotate([90,0,0])
    cylinder(r=normal_screw_r, h=insert_thickess/2, center=true);
    
    color("gold")
    translate([holder_spacing_from_center,
               0,
               -z_offset - normal_screw_r
             ])
    rotate([90,0,0])
    cylinder(r=screw_r, h=insert_thickess, center=true);
    
    color("red")
    translate([holder_spacing_from_center,
               insert_thickess/4,
               -z_offset - normal_screw_r
             ])
    rotate([90,0,0])
    cylinder(r=normal_screw_r, h=insert_thickess/2, center=true);
}