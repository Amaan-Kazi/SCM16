module SCM16 (clk, rst);
  parameter UUID = 0;
  parameter NAME = "";
  input wire clk;
  input wire rst;


  TC_Program # (.UUID(64'd3036675205634735936 ^ UUID), .WORD_WIDTH(64'd16), .DEFAULT_FILE_NAME("Program_2A247002B2183F40.w16.bin"), .ARG_SIG("Program_2A247002B2183F40=%s")) Program_0 (.clk(clk), .rst(rst), .address(wire_79), .out0(wire_0), .out1(wire_15), .out2(wire_12), .out3(wire_33));
  TC_Counter # (.UUID(64'd3613463651816973605 ^ UUID), .BIT_WIDTH(64'd16), .count(16'd4)) Counter16_1 (.clk(clk), .rst(rst), .save(wire_43), .in(wire_7), .out(wire_79));
  TC_Ram # (.UUID(64'd3779316721177258366 ^ UUID), .WORD_WIDTH(64'd16), .WORD_COUNT(64'd65536)) Ram_2 (.clk(clk), .rst(rst), .load(1'd0), .save(1'd0), .address(32'd0), .in0(64'd0), .in1(64'd0), .in2(64'd0), .in3(64'd0), .out0(), .out1(), .out2(), .out3());
  TC_Splitter16 # (.UUID(64'd1964885700083813915 ^ UUID)) Splitter16_3 (.in(wire_0[15:0]), .out0(), .out1(wire_56));
  TC_Splitter8 # (.UUID(64'd2865909427779811686 ^ UUID)) Splitter8_4 (.in(wire_78), .out0(), .out1(), .out2(), .out3(), .out4(wire_65), .out5(wire_13), .out6(wire_30), .out7(wire_39));
  TC_Register # (.UUID(64'd1768297580719965166 ^ UUID), .BIT_WIDTH(64'd16)) Register16_5 (.clk(clk), .rst(rst), .load(wire_62), .save(wire_60), .in(wire_19), .out(wire_51));
  TC_Register # (.UUID(64'd12270441446668041 ^ UUID), .BIT_WIDTH(64'd16)) Register16_6 (.clk(clk), .rst(rst), .load(wire_69), .save(wire_5), .in(wire_19), .out(wire_36));
  TC_Register # (.UUID(64'd3602252881066521773 ^ UUID), .BIT_WIDTH(64'd16)) Register16_7 (.clk(clk), .rst(rst), .load(wire_46), .save(wire_63), .in(wire_19), .out(wire_27));
  TC_Register # (.UUID(64'd937036284257795972 ^ UUID), .BIT_WIDTH(64'd16)) Register16_8 (.clk(clk), .rst(rst), .load(wire_58), .save(wire_49), .in(wire_19), .out(wire_77));
  TC_Register # (.UUID(64'd1771485704314964723 ^ UUID), .BIT_WIDTH(64'd16)) Register16_9 (.clk(clk), .rst(rst), .load(wire_59), .save(wire_31), .in(wire_19), .out(wire_64));
  TC_Register # (.UUID(64'd1030977193978425972 ^ UUID), .BIT_WIDTH(64'd16)) Register16_10 (.clk(clk), .rst(rst), .load(wire_71), .save(wire_53), .in(wire_19), .out(wire_29));
  TC_Register # (.UUID(64'd1897207591897939717 ^ UUID), .BIT_WIDTH(64'd16)) Register16_11 (.clk(clk), .rst(rst), .load(wire_66), .save(wire_34), .in(wire_19), .out(wire_48));
  TC_Console # (.UUID(64'd1550364046122691923 ^ UUID)) Console_12 (.clk(clk), .rst(rst), .offset(32'd0));
  TC_Splitter16 # (.UUID(64'd1676756795661497062 ^ UUID)) Splitter16_13 (.in(wire_15[15:0]), .out0(wire_21), .out1());
  TC_Splitter16 # (.UUID(64'd2723123645093883319 ^ UUID)) Splitter16_14 (.in(wire_12[15:0]), .out0(wire_73), .out1());
  TC_Or # (.UUID(64'd3489109707031568152 ^ UUID), .BIT_WIDTH(64'd1)) Or_15 (.in0(wire_8), .in1(wire_10), .out(wire_2));
  TC_Or # (.UUID(64'd2757568662684548394 ^ UUID), .BIT_WIDTH(64'd1)) Or_16 (.in0(wire_41), .in1(wire_6), .out(wire_62));
  TC_Or # (.UUID(64'd2444150779797091056 ^ UUID), .BIT_WIDTH(64'd1)) Or_17 (.in0(wire_22), .in1(wire_16), .out(wire_69));
  TC_Or # (.UUID(64'd3998494940572441480 ^ UUID), .BIT_WIDTH(64'd1)) Or_18 (.in0(wire_57), .in1(wire_68), .out(wire_46));
  TC_Or # (.UUID(64'd3745487864523206918 ^ UUID), .BIT_WIDTH(64'd1)) Or_19 (.in0(wire_11), .in1(wire_18), .out(wire_58));
  TC_Or # (.UUID(64'd151306593792916243 ^ UUID), .BIT_WIDTH(64'd1)) Or_20 (.in0(wire_50), .in1(wire_40), .out(wire_59));
  TC_Or # (.UUID(64'd3493104666195700629 ^ UUID), .BIT_WIDTH(64'd1)) Or_21 (.in0(wire_54), .in1(wire_1), .out(wire_71));
  TC_Or # (.UUID(64'd3870924515638343503 ^ UUID), .BIT_WIDTH(64'd1)) Or_22 (.in0(wire_26), .in1(wire_20), .out(wire_66));
  TC_Splitter8 # (.UUID(64'd2466557324773763251 ^ UUID)) Splitter8_23 (.in(wire_21), .out0(wire_23), .out1(wire_76), .out2(wire_67), .out3(wire_70), .out4(), .out5(), .out6(), .out7());
  TC_Splitter8 # (.UUID(64'd1977466255751035882 ^ UUID)) Splitter8_24 (.in(wire_73), .out0(wire_80), .out1(wire_72), .out2(wire_42), .out3(wire_35), .out4(), .out5(), .out6(), .out7());
  TC_Splitter16 # (.UUID(64'd2261501443814513651 ^ UUID)) Splitter16_25 (.in(wire_33[15:0]), .out0(wire_55), .out1());
  TC_Splitter8 # (.UUID(64'd2576232014769382965 ^ UUID)) Splitter8_26 (.in(wire_55), .out0(wire_75), .out1(wire_81), .out2(wire_38), .out3(wire_47), .out4(), .out5(), .out6(), .out7());
  TC_Switch # (.UUID(64'd2608661849516270155 ^ UUID), .BIT_WIDTH(64'd16)) Switch16_27 (.en(wire_10), .in(wire_9), .out(wire_3_7));
  TC_Switch # (.UUID(64'd746143341221514145 ^ UUID), .BIT_WIDTH(64'd16)) Switch16_28 (.en(wire_8), .in(wire_9), .out(wire_4_7));
  TC_Switch # (.UUID(64'd2038162143482139082 ^ UUID), .BIT_WIDTH(64'd16)) Switch16_29 (.en(wire_6), .in(wire_51), .out(wire_3_6));
  TC_Switch # (.UUID(64'd4451929975376370007 ^ UUID), .BIT_WIDTH(64'd16)) Switch16_30 (.en(wire_41), .in(wire_51), .out(wire_4_6));
  TC_Switch # (.UUID(64'd2149760867058136119 ^ UUID), .BIT_WIDTH(64'd16)) Switch16_31 (.en(wire_16), .in(wire_36), .out(wire_3_4));
  TC_Switch # (.UUID(64'd1120920137235279511 ^ UUID), .BIT_WIDTH(64'd16)) Switch16_32 (.en(wire_22), .in(wire_36), .out(wire_4_5));
  TC_Switch # (.UUID(64'd1049077220225763239 ^ UUID), .BIT_WIDTH(64'd16)) Switch16_33 (.en(wire_68), .in(wire_27), .out(wire_3_2));
  TC_Switch # (.UUID(64'd690331529650965982 ^ UUID), .BIT_WIDTH(64'd16)) Switch16_34 (.en(wire_57), .in(wire_27), .out(wire_4_4));
  TC_Switch # (.UUID(64'd4446234359163774586 ^ UUID), .BIT_WIDTH(64'd16)) Switch16_35 (.en(wire_18), .in(wire_77), .out(wire_3_0));
  TC_Switch # (.UUID(64'd68561501764135042 ^ UUID), .BIT_WIDTH(64'd16)) Switch16_36 (.en(wire_11), .in(wire_77), .out(wire_4_3));
  TC_Switch # (.UUID(64'd2300663947791505692 ^ UUID), .BIT_WIDTH(64'd16)) Switch16_37 (.en(wire_40), .in(wire_64), .out(wire_3_1));
  TC_Switch # (.UUID(64'd1809390294038489791 ^ UUID), .BIT_WIDTH(64'd16)) Switch16_38 (.en(wire_50), .in(wire_64), .out(wire_4_2));
  TC_Switch # (.UUID(64'd2131531128077507626 ^ UUID), .BIT_WIDTH(64'd16)) Switch16_39 (.en(wire_1), .in(wire_29), .out(wire_3_3));
  TC_Switch # (.UUID(64'd2315389642693555300 ^ UUID), .BIT_WIDTH(64'd16)) Switch16_40 (.en(wire_54), .in(wire_29), .out(wire_4_1));
  TC_Switch # (.UUID(64'd4187739606022409523 ^ UUID), .BIT_WIDTH(64'd16)) Switch16_41 (.en(wire_20), .in(wire_48), .out(wire_3_5));
  TC_Switch # (.UUID(64'd1859071114078130426 ^ UUID), .BIT_WIDTH(64'd16)) Switch16_42 (.en(wire_26), .in(wire_48), .out(wire_4_0));
  TC_Equal # (.UUID(64'd137163679941758477 ^ UUID), .BIT_WIDTH(64'd16)) Equal16_43 (.in0(wire_0[15:0]), .in1(wire_28), .out(wire_32));
  TC_Halt # (.UUID(64'd2683931794444888664 ^ UUID)) Halt_44 (.clk(clk), .rst(rst), .en(wire_32));
  TC_Constant # (.UUID(64'd1352990490392554841 ^ UUID), .BIT_WIDTH(64'd16), .value(16'hFFFF)) Constant16_45 (.out(wire_28));
  TC_Switch # (.UUID(64'd971606683869478136 ^ UUID), .BIT_WIDTH(64'd16)) Switch16_46 (.en(wire_30), .in(wire_12[15:0]), .out(wire_3_8));
  TC_Switch # (.UUID(64'd488700789590138722 ^ UUID), .BIT_WIDTH(64'd16)) Switch16_47 (.en(wire_39), .in(wire_15[15:0]), .out(wire_4_8));
  TC_Constant # (.UUID(64'd1219804294531623130 ^ UUID), .BIT_WIDTH(64'd16), .value(16'h0)) Constant16_48 (.out(wire_9));
  TC_Switch # (.UUID(64'd2854432665896608476 ^ UUID), .BIT_WIDTH(64'd8)) Switch8_49 (.en(wire_61), .in(wire_56), .out(wire_78));
  TC_Not # (.UUID(64'd1919204710248089503 ^ UUID), .BIT_WIDTH(64'd1)) Not_50 (.in(wire_32), .out(wire_61));
  TC_Register # (.UUID(64'd4051416113551873170 ^ UUID), .BIT_WIDTH(64'd16)) Register16_51 (.clk(clk), .rst(rst), .load(wire_37), .save(wire_24), .in(wire_19), .out(wire_25));
  TC_Switch # (.UUID(64'd3648642341737646920 ^ UUID), .BIT_WIDTH(64'd16)) Switch16_52 (.en(wire_43), .in(wire_25), .out(wire_7));
  TC_Switch # (.UUID(64'd2839537485959427856 ^ UUID), .BIT_WIDTH(64'd1)) Switch1_53 (.en(wire_37), .in(wire_37), .out(wire_43));
  TC_Switch # (.UUID(64'd1274280706530208026 ^ UUID), .BIT_WIDTH(64'd16)) Switch16_54 (.en(wire_37), .in(wire_52), .out(wire_19_1));
  DEC4 # (.UUID(64'd606098422439323267 ^ UUID)) DEC4_55 (.clk(clk), .rst(rst), .Bit_1(wire_23), .Bit_2(wire_76), .Bit_3(wire_67), .Bit_4(wire_70), .Disable(wire_39), .Output_1(wire_50), .Output_2(wire_54), .Output_3(wire_26), .Output_4(wire_11), .Output_5(wire_57), .Output_6(wire_22), .Output_7(wire_41), .Output_8(wire_8), .Output_9(), .Output_10(), .Output_11(), .Output_12(), .Output_13(), .Output_14(), .Output_15(), .Output_16());
  DEC4 # (.UUID(64'd2350125178974466839 ^ UUID)) DEC4_56 (.clk(clk), .rst(rst), .Bit_1(wire_80), .Bit_2(wire_72), .Bit_3(wire_42), .Bit_4(wire_35), .Disable(wire_30), .Output_1(wire_40), .Output_2(wire_1), .Output_3(wire_20), .Output_4(wire_18), .Output_5(wire_68), .Output_6(wire_16), .Output_7(wire_6), .Output_8(wire_10), .Output_9(), .Output_10(), .Output_11(), .Output_12(), .Output_13(), .Output_14(), .Output_15(), .Output_16());
  DEC4 # (.UUID(64'd4239434022177334522 ^ UUID)) DEC4_57 (.clk(clk), .rst(rst), .Bit_1(wire_75), .Bit_2(wire_81), .Bit_3(wire_38), .Bit_4(wire_47), .Disable(1'd0), .Output_1(wire_31), .Output_2(wire_53), .Output_3(wire_34), .Output_4(wire_49), .Output_5(wire_63), .Output_6(wire_5), .Output_7(wire_60), .Output_8(wire_45), .Output_9(), .Output_10(), .Output_11(), .Output_12(), .Output_13(), .Output_14(wire_24), .Output_15(), .Output_16());
  ALU # (.UUID(64'd1759242323400889102 ^ UUID)) ALU_58 (.clk(clk), .rst(rst), .Instruction(wire_0[15:0]), .Input_1(wire_4), .Input_2(wire_3), .Enable(wire_14), .Output(wire_19_0));
  DEC2 # (.UUID(64'd2289023201248810830 ^ UUID)) DEC2_59 (.clk(clk), .rst(rst), .Input_1(wire_65), .Input_2(wire_13), .Disable(wire_32), .Output_1(wire_44), .Output_2(wire_74), .Output_3(wire_17), .Output_4(wire_14));
  COND # (.UUID(64'd651755983125011903 ^ UUID)) COND_60 (.clk(clk), .rst(rst), .Instruction(wire_0[15:0]), .Input_1(wire_4), .Input_2(wire_3), .Enable(wire_44), .Output(wire_37));
  TC_Constant # (.UUID(64'd935331273960341813 ^ UUID), .BIT_WIDTH(64'd16), .value(16'h1)) Constant16_61 (.out(wire_52));

  wire [63:0] wire_0;
  wire [0:0] wire_1;
  wire [0:0] wire_2;
  wire [15:0] wire_3;
  wire [15:0] wire_3_0;
  wire [15:0] wire_3_1;
  wire [15:0] wire_3_2;
  wire [15:0] wire_3_3;
  wire [15:0] wire_3_4;
  wire [15:0] wire_3_5;
  wire [15:0] wire_3_6;
  wire [15:0] wire_3_7;
  wire [15:0] wire_3_8;
  assign wire_3 = wire_3_0|wire_3_1|wire_3_2|wire_3_3|wire_3_4|wire_3_5|wire_3_6|wire_3_7|wire_3_8;
  wire [15:0] wire_4;
  wire [15:0] wire_4_0;
  wire [15:0] wire_4_1;
  wire [15:0] wire_4_2;
  wire [15:0] wire_4_3;
  wire [15:0] wire_4_4;
  wire [15:0] wire_4_5;
  wire [15:0] wire_4_6;
  wire [15:0] wire_4_7;
  wire [15:0] wire_4_8;
  assign wire_4 = wire_4_0|wire_4_1|wire_4_2|wire_4_3|wire_4_4|wire_4_5|wire_4_6|wire_4_7|wire_4_8;
  wire [0:0] wire_5;
  wire [0:0] wire_6;
  wire [15:0] wire_7;
  wire [0:0] wire_8;
  wire [15:0] wire_9;
  wire [0:0] wire_10;
  wire [0:0] wire_11;
  wire [63:0] wire_12;
  wire [0:0] wire_13;
  wire [0:0] wire_14;
  wire [63:0] wire_15;
  wire [0:0] wire_16;
  wire [0:0] wire_17;
  wire [0:0] wire_18;
  wire [15:0] wire_19;
  wire [15:0] wire_19_0;
  wire [15:0] wire_19_1;
  assign wire_19 = wire_19_0|wire_19_1;
  wire [0:0] wire_20;
  wire [7:0] wire_21;
  wire [0:0] wire_22;
  wire [0:0] wire_23;
  wire [0:0] wire_24;
  wire [15:0] wire_25;
  wire [0:0] wire_26;
  wire [15:0] wire_27;
  wire [15:0] wire_28;
  wire [15:0] wire_29;
  wire [0:0] wire_30;
  wire [0:0] wire_31;
  wire [0:0] wire_32;
  wire [63:0] wire_33;
  wire [0:0] wire_34;
  wire [0:0] wire_35;
  wire [15:0] wire_36;
  wire [0:0] wire_37;
  wire [0:0] wire_38;
  wire [0:0] wire_39;
  wire [0:0] wire_40;
  wire [0:0] wire_41;
  wire [0:0] wire_42;
  wire [0:0] wire_43;
  wire [0:0] wire_44;
  wire [0:0] wire_45;
  wire [0:0] wire_46;
  wire [0:0] wire_47;
  wire [15:0] wire_48;
  wire [0:0] wire_49;
  wire [0:0] wire_50;
  wire [15:0] wire_51;
  wire [15:0] wire_52;
  wire [0:0] wire_53;
  wire [0:0] wire_54;
  wire [7:0] wire_55;
  wire [7:0] wire_56;
  wire [0:0] wire_57;
  wire [0:0] wire_58;
  wire [0:0] wire_59;
  wire [0:0] wire_60;
  wire [0:0] wire_61;
  wire [0:0] wire_62;
  wire [0:0] wire_63;
  wire [15:0] wire_64;
  wire [0:0] wire_65;
  wire [0:0] wire_66;
  wire [0:0] wire_67;
  wire [0:0] wire_68;
  wire [0:0] wire_69;
  wire [0:0] wire_70;
  wire [0:0] wire_71;
  wire [0:0] wire_72;
  wire [7:0] wire_73;
  wire [0:0] wire_74;
  wire [0:0] wire_75;
  wire [0:0] wire_76;
  wire [15:0] wire_77;
  wire [7:0] wire_78;
  wire [15:0] wire_79;
  wire [0:0] wire_80;
  wire [0:0] wire_81;

endmodule