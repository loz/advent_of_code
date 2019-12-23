require "spec"
require "./spec_helper"

describe IOPipe do
  it "can have data put in and out" do
    pipe = IOPipe.new
    pipe << 1234.to_i64
    pipe.shift.should eq 1234.to_i64
  end

  it "blocks a read until data arrives" do
    pipe = IOPipe.new
    spawn do
      read = pipe.shift
      read.should eq 1234.to_i64
    end
    sleep 1.seconds
    pipe << 1234.to_i64
  end
end
