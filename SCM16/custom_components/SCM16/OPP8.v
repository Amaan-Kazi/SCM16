module OPP8 (clk, rst, Input_1, Input_2, Input_3, Input_4, Input_5, Input_6, Input_7, Input_8, Output_1, Output_2, Output_3, Output_4, Output_5, Output_6, Output_7, Output_8);
  parameter UUID = 0;
  parameter NAME = "";
  input wire clk;
  input wire rst;

  input  wire [0:0] Input_1;
  input  wire [0:0] Input_2;
  input  wire [0:0] Input_3;
  input  wire [0:0] Input_4;
  input  wire [0:0] Input_5;
  input  wire [0:0] Input_6;
  input  wire [0:0] Input_7;
  input  wire [0:0] Input_8;
  output  wire [0:0] Output_1;
  output  wire [0:0] Output_2;
  output  wire [0:0] Output_3;
  output  wire [0:0] Output_4;
  output  wire [0:0] Output_5;
  output  wire [0:0] Output_6;
  output  wire [0:0] Output_7;
  output  wire [0:0] Output_8;

  TC_Maker16 # (.UUID(64'd4576894713119714030 ^ UUID)) Maker16_0 (.in0(8'd0), .in1(8'd0), .out());
  TC_Maker16 # (.UUID(64'd4159457257671284809 ^ UUID)) Maker16_1 (.in0(8'd0), .in1(8'd0), .out());
  TC_Maker16 # (.UUID(64'd135754618811469109 ^ UUID)) Maker16_2 (.in0(8'd0), .in1(8'd0), .out());
  TC_Maker16 # (.UUID(64'd2144888840407442937 ^ UUID)) Maker16_3 (.in0(8'd0), .in1(8'd0), .out());
  TC_Maker16 # (.UUID(64'd1923742623033063111 ^ UUID)) Maker16_4 (.in0(8'd0), .in1(8'd0), .out());
  TC_Maker16 # (.UUID(64'd2531585302615411283 ^ UUID)) Maker16_5 (.in0(8'd0), .in1(8'd0), .out());
  TC_Maker16 # (.UUID(64'd1446271324425451477 ^ UUID)) Maker16_6 (.in0(8'd0), .in1(8'd0), .out());
  TC_Maker16 # (.UUID(64'd971499438910037494 ^ UUID)) Maker16_7 (.in0(8'd0), .in1(8'd0), .out());

  wire [0:0] wire_0;
  assign wire_0 = Input_5;
  assign Output_4 = wire_0;
  wire [0:0] wire_1;
  assign wire_1 = Input_2;
  assign Output_7 = wire_1;
  wire [0:0] wire_2;
  assign wire_2 = Input_3;
  assign Output_6 = wire_2;
  wire [0:0] wire_3;
  assign wire_3 = Input_7;
  assign Output_2 = wire_3;
  wire [0:0] wire_4;
  assign wire_4 = Input_8;
  assign Output_1 = wire_4;
  wire [0:0] wire_5;
  assign wire_5 = Input_4;
  assign Output_5 = wire_5;
  wire [0:0] wire_6;
  assign wire_6 = Input_1;
  assign Output_8 = wire_6;
  wire [0:0] wire_7;
  assign wire_7 = Input_6;
  assign Output_3 = wire_7;

endmodule
