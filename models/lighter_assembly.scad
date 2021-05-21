use <bottle_adapter.scad>

$fn=60;

ligther_y = 16;

assembly_x = 40;
assembly_y = 36;

width = 10;
z = 7;

servo_cable_channel_x = 10;
servo_cable_channel_y = 14;
servo_cable_channel_z = 5;

servo_y = 12;
servo_x = 20;
servo_z = 40;

screw_insert_depth = 2;

servo_attachment_dist = 6;
servo_attachment_offset = 4;
screw_r = 2/2;


difference(){
    union(){
    // left - top view
    translate([-assembly_x/2 - width,-width,0])
    cube([width,assembly_y + width,z]);

    // top - top view
    translate([-assembly_x/2,-width,0])
    cube([assembly_x,width,z]);

    // right - top view
    translate([assembly_x/2,-width,0])
    cube([width,assembly_y + width,z]);
    }
    
    // servo
    color("gold")
    translate([-assembly_x/2,
               ligther_y + width,
               z-screw_insert_depth
             ])
    rotate([90,0,90])
    servo_insert();
    
    //servo cable cutout
    translate([-servo_x - servo_cable_channel_x,22.5,0])
    color("gold")
    cube([servo_cable_channel_x,servo_cable_channel_y,z]);
    
    color("red")
translate([-assembly_x/2 - width + servo_attachment_offset,-1,z/2])
rotate([90,0,0])
cylinder(r=screw_r,h=width-1);

color("red")
translate([-assembly_x/2 - width + servo_attachment_offset + servo_attachment_dist,-1,z/2])
rotate([90,0,0])
cylinder(r=screw_r,h=width-1);

}


