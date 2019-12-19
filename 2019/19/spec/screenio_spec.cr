require "spec"
require "./spec_helper"

describe ScreenIO do
  it "put empty tile at x,y" do
    screen = ScreenIO.new
    screen << 10.to_i64
    screen << 24.to_i64
    screen << 0.to_i64
    screen.at(10,24).should eq :empty
  end

  it "put wall tile at x,y" do
    screen = ScreenIO.new
    screen << 13.to_i64
    screen << 21.to_i64
    screen << 1.to_i64
    screen.at(13,21).should eq :wall
  end

  it "will handle score" do
    screen = ScreenIO.new
    screen << -1.to_i64
    screen << 0.to_i64
    screen << 2435.to_i64

    screen.score.should eq 2435.to_i64
  end
end
