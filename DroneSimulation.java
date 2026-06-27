package drone;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

import javax.swing.JFrame;
import javax.swing.JPanel;

public class Main extends JPanel implements Runnable {
	
	public class Body{
		double x, y;
		double velX, velY;
		
		double angle;
		double angleVel;
		
		double mass;
		double inertia;
		
		int width;
		int height;
		
		public Body(double X, double Y, double angle, int width, int height, double mass) {
			this.x = X;		this.y = Y;
			this.width = width;	this.height = height;
			this.mass = mass;

			this.inertia = mass * (width*width + height*height) / 12.0;
			this.angle = angle;	this.angleVel = 0;
		    this.velY = 0;	this.velX = 0;
		}
		
		public static double[] getWorldPoint(
		        double x_local, double y_local,
		        double theta,
		        double x_COM, double y_COM) {

		    double cos = Math.cos(theta);
		    double sin = Math.sin(theta);

		    double x_rot = x_local * cos - y_local * sin;
		    double y_rot = x_local * sin + y_local * cos;

		    double x_world = x_COM + x_rot;
		    double y_world = y_COM + y_rot;

		    return new double[]{x_world, y_world};
		}
		
		public double[] getVelocityAtPoint(double rx, double ry) {
		    double vx = velX - angleVel * ry;
		    double vy = velY + angleVel * rx;
		    return new double[]{vx, vy};
		}
	}
	
    Body drone = new Body(250, 100, 0, 50, 6, 0.7);

    final double gravity = 0.3;
    final double thrust = 0.16;
    final double drag = 0.97;
    final double angularDrag = 0.95;

    boolean upPressed = false;
    boolean leftPressed = false;
    boolean rightPressed = false;
    boolean downPressed = false;

    int screenHeight, screenWidth;
	
	public Main(int screenWidth, int screenHeight) {
		this.screenHeight = screenHeight;
		this.screenWidth = screenWidth;        
		
		setBackground(Color.WHITE);

        setFocusable(true);
        addKeyListener(new KeyAdapter() {
            public void keyPressed(KeyEvent e) {
                if (e.getKeyCode() == KeyEvent.VK_UP) upPressed = true;
                if (e.getKeyCode() == KeyEvent.VK_LEFT) leftPressed = true;
                if (e.getKeyCode() == KeyEvent.VK_RIGHT) rightPressed = true;
                if (e.getKeyCode() == KeyEvent.VK_DOWN) downPressed = true;
            }
            public void keyReleased(KeyEvent e) {
                if (e.getKeyCode() == KeyEvent.VK_UP) upPressed = false;
                if (e.getKeyCode() == KeyEvent.VK_LEFT) leftPressed = false;
                if (e.getKeyCode() == KeyEvent.VK_RIGHT) rightPressed = false;
                if (e.getKeyCode() == KeyEvent.VK_DOWN) downPressed = false;
            }
        });
    }
    
    @Override
    protected void paintComponent(Graphics g) {
    	super.paintComponent(g);
    	
    	Graphics2D g2 = (Graphics2D) g;

        double angle = drone.angle; 
        
    	g.drawLine(0, 250, 500, 250);
    	g.drawLine(250, 0, 250, 500);
    	
        g.setColor(Color.BLACK);
        g2.rotate(angle, drone.x, drone.y);
        g.fillRect((int)(drone.x-drone.width/2), (int)(drone.y-drone.height/2), drone.width, drone.height);
        g2.rotate(-angle, drone.x, drone.y);
    }

    @Override
    public void run() {
        while (true) {
                        

            drone.velY += gravity;

            drone.x += drone.velX;
            drone.y += drone.velY;
            drone.angle += drone.angleVel;

            drone.velX *= drag;
            drone.velY *= drag;
            drone.angleVel *= angularDrag;
            	
            double hw = drone.width / 2.0;
            double hh = drone.height / 2.0;

            double[][] corners = {
                {-hw, -hh},
                { hw, -hh},
                { hw,  hh},
                {-hw,  hh}
            };

            double groundY = screenHeight - 100;
            double e = 0.4;
        	
            for (int i = 0; i < 4; i++) {

                double[] p = Body.getWorldPoint(
                        corners[i][0], corners[i][1],
                        drone.angle,
                        drone.x, drone.y);

                double px = p[0];
                double py = p[1];
                
                double rx = px - drone.x;
                double ry = py - drone.y;

                double[] v = drone.getVelocityAtPoint(rx, ry);
                double vx = v[0];
                double vy = v[1];
                
                if(i == 0 || i == 1) {
                	
                	double nx = Math.sin(drone.angle);
                	double ny = -Math.cos(drone.angle);

                	
                    if(leftPressed && i == 0) {
                    	
                    	double torque = rx * (thrust * ny) - ry * (thrust * nx);
                    	drone.angleVel -= (torque*0.3 / drone.inertia);
                    	
                	}else if(rightPressed && i == 1){                	
                    	double torque = rx * (thrust * ny) - ry * (thrust * nx);
                    	drone.angleVel -= (torque*0.3 / drone.inertia);
                    	
                	}else if(upPressed) {
                		drone.velX += thrust * nx / drone.mass;
                    	drone.velY += thrust * ny / drone.mass;
                    	
                    }else if(downPressed) {
                    	drone.velX -= thrust * nx / drone.mass;
                    	drone.velY -= thrust * ny / drone.mass;
                    }
                }
                
                if (py >= groundY) {

                    double nx = 0;
                    double ny = -1;
                    
                    double vDotN = vx * nx + vy * ny;
                    if (vDotN > 0) continue;

                    double rCrossN = rx * ny - ry * nx;

                    double j = -(1 + e) * vDotN /
                            (1.0 / drone.mass + (rCrossN * rCrossN) / drone.inertia);

                    drone.velX += (j * nx) / drone.mass;
                    drone.velY += (j * ny) / drone.mass;

                    double torque = rx * (j * ny) - ry * (j * nx);
                    drone.angleVel += torque / drone.inertia;

                    drone.y -= (py - groundY);
                }
            }

            repaint();
            try { Thread.sleep(10); } catch (Exception ignored) {}
        }
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("Drone Control");
        int screenWidth = 600, screenHeight = 600;
        Main panel = new Main(screenHeight, screenHeight);
        frame.add(panel);
        frame.setSize(screenWidth, screenHeight);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
        panel.requestFocusInWindow();
        new Thread(panel).start();
    }
}
