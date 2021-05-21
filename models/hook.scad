$fn=60;

hook_z = 20;
cutout_cube = 10;


difference(){
    linear_extrude(hook_z)
    import("hook.svg");

    translate([cutout_cube/2,           cutout_cube/3,
               cutout_cube/2])
    cube(cutout_cube);
}

