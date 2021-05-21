$fn= 60;

x_dist = 58;
y_dist = 23;

x_base = x_dist;
y_base = y_dist;
z_base = 4;

difference(){
    base();
    base_holes();
    base_text();
}

module base(){
    r_corner = 3;

    hull(){
        cube([x_base, y_base, z_base]);
            cylinder(r=r_corner, h=z_base);
            
            translate([x_dist,0,0])
            cylinder(r=r_corner, h=z_base);
            
            translate([x_dist,y_dist,0])
            cylinder(r=r_corner, h=z_base);
            
            translate([0,y_dist,0])
            cylinder(r=r_corner, h=z_base);
        }
}

module base_holes(){
    r = 2.75/2;
    
    h_under = 2;
    r_under = 5/2;

    cylinder(r=r, h=z_base);
    cylinder(r=r_under, h=h_under);


    translate([x_dist,0,0]){
        cylinder(r=r, h=z_base);
        cylinder(r=r_under, h=h_under);
    }


    translate([0,y_dist,0]){
        cylinder(r=r, h=z_base);
        cylinder(r=r_under, h=h_under);
    }


    translate([x_dist,y_dist,0]){
        cylinder(r=r, h=z_base);
        cylinder(r=r_under, h=h_under);
    }
}

module base_text(){
    translate([x_dist/2,y_dist/2,2])
    linear_extrude(2)
    text("YT/ALFREDOSEQUEIDA", size=4, valign="center", halign="center", font="roboto:style=Bold");
}