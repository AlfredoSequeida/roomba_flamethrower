$fn=60;

x = 3;
y = 3;
z = 8;
r = 10;

top_z = 16;
top_r = 40/2;

difference(){
translate([0,0,top_z + y])
rotate([180,0,0])
cap();

translate([0,0,top_z + y -0.5])
linear_extrude(3)
text("2.8", size=9, halign="center", valign="center");
}
module cap(){
    difference(){
        hull(){
            translate([0,0,top_z])
            cylinder(r=top_r, 3);
            cylinder(r=r,h=z);
        }
        nozzle();
    }
}

module nozzle(){
    insert_h = 13;
    nozzle_r = 2.8/2;

    insert_padding = 0.1;
    prism_s = nozzle_r*2;

    union(){
        cylinder(r=nozzle_r + insert_padding,h=insert_h);

        translate([0,0,insert_h])
        sphere(r=nozzle_r + insert_padding);
        
        translate([0,0,insert_h])
        rotate([90,0,0])
        cylinder(r=nozzle_r + insert_padding,h=insert_h + 10);
    }
}