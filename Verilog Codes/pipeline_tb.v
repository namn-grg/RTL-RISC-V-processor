module tb();

    reg clk=1'b0, rst;
//    wire WE,RegWriteW,ALUSrcE,ResultSrcE,MemWriteE,BranchE,RegWriteE,PCSrC,PCSrcE,RegWriteM,MemWriteM,ResultSrcM,ResultSrcW;
//    wire [1:0] ForwardA_E, ForwardB_E;
//    wire [31:0] A,WD,RD,B,InstrD,PCD,PCPlus4D,ResultW,RD1_E,RD2_E,Imm_Ext_E,PCE,PCPlus4E,PCTargetE,PCPlus4M,WriteDataM,ALU_ResultM,PCPlus4W,ALU_ResultW,ReadDataW;
//    wire [4:0] RDW, RS1_E, RS2_E, RD_E,RD_M,RD_W;
//    wire [2:0] ALUControlE;
    
    
    
    always begin
    forever
    begin
          clk = ~clk;
          #50;
         end
        
    end

    initial begin
        rst <= 1'b0;
        #200;
        rst <= 1'b1;
        #1000;
        
        $finish;    
    end

    initial begin
        
        $dumpfile("dump.vcd");
        $dumpvars(0);
    end

    Pipeline_top dut (.clk(clk), .rst(rst));
    
//    fetch_cycle dut1 (.clk(clk),.rst(rst),.PCSrcE(PCSrcE),.PCTargetE(PCTargetE),.InstrD(InstrD),.PCD(PCD),.PCPlus4D(PCPlus4D));
//    decode_cycle dut2 (clk, rst, InstrD, PCD, PCPlus4D, RegWriteW, RDW, ResultW, RegWriteE, ALUSrcE, MemWriteE, ResultSrcE,
//    BranchE,  ALUControlE, RD1_E, RD2_E, Imm_Ext_E, RD_E, PCE, PCPlus4E, RS1_E, RS2_E);
//    execute_cycle dut3 (clk, rst, RegWriteE, ALUSrcE, MemWriteE, ResultSrcE, BranchE, ALUControlE,RD1_E, RD2_E, Imm_Ext_E, RD_E, PCE, PCPlus4E, PCSrcE, PCTargetE, RegWriteM, MemWriteM, ResultSrcM, RD_M, PCPlus4M, WriteDataM, ALU_ResultM, ResultW, ForwardA_E, ForwardB_E);
//    memory_cycle dut4 (clk, rst, RegWriteM, MemWriteM, ResultSrcM, RD_M, PCPlus4M, WriteDataM, 
//    ALU_ResultM, RegWriteW, ResultSrcW, RD_W, PCPlus4W, ALU_ResultW, ReadDataW);
//    writeback_cycle dut5 (clk, rst, ResultSrcW, PCPlus4W, ALU_ResultW, ReadDataW, ResultW);
//    Instruction_Memory in (.rst(rst),.A(A),.RD(RD));
//    Data_Memory in1 (.clk(clk),.rst(rst),.WE(WE),.WD(WD),.A(A),.RD(RD));
    
    
    
endmodule