$fn=60;
bottle_r = 53/2;
insert_padding = 0.1;

stand_h = 30;
thickness = 3;

difference(){
    cylinder(r=bottle_r + thickness,h=stand_h);
    translate([0,0,thickness])
    cylinder(r=bottle_r + insert_padding,h=stand_h);
    
    translate([0,0,thickness + stand_h/2])
    cube([10,100,10],center=true);
}