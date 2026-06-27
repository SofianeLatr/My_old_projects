import java.sql.*;
import java.util.Scanner;

public class JDBC {
	
	static String url = "jdbc:mysql://localhost:3306/jdbc";
	static String user = "root";
	static String password = "";
	
	public static void main(String[] args) {
		
		Scanner sc = new Scanner(System.in);
		try(Connection conn = DriverManager.getConnection(url, user, password)){
            
			Boolean running = true;
			while(running) {
				System.out.println("\n========= MENU =========");
	            System.out.println("1. View all employees");
	            System.out.println("2. Add employee");
	            System.out.println("3. Update employee");
	            System.out.println("4. Delete employee");
	            System.out.println("5. Exit");
	            System.out.print("Choose: ");
	            
	            int input = sc.nextInt();
	            sc.nextLine();
	           
	            switch(input) {
	            	case 1 -> viewEmployees(conn);
	            	case 2 -> addEmployee(sc, conn);
	            	case 3 -> updateEmployee(sc, conn);
	            	case 4 -> deleteEmployee(sc,conn);
	            	case 5 -> {running = false;}
	            }
	            
			}
            
		}catch(SQLException e) {
			e.printStackTrace();
		}
	}
	
	static public void viewEmployees(Connection conn) throws SQLException{
		ResultSet output = conn.createStatement().executeQuery("SELECT * FROM employees");
		System.out.println("\n");
		while(output.next()) {
			System.out.println("id: " + output.getInt("id")+ " name: "+ output.getString("name"));
		}
	}
	static public void addEmployee(Scanner sc, Connection conn) throws SQLException {
		System.out.println("\n");
		System.out.println("Enter the employee name: ");
		String name = sc.nextLine();
		
		PreparedStatement st = conn.prepareStatement("INSERT INTO employees (name) VALUES (?)");
		st.setString(1, name);
		int rows = st.executeUpdate();
		System.out.println(rows + " row(s) added");
	}
	static public void updateEmployee(Scanner sc, Connection conn) throws SQLException{
		System.out.println("\n");
		System.out.println("Enter the id of the employee to update: ");
		int id = sc.nextInt();
		sc.nextLine();
		System.out.println("Enter the new employee name: ");
		String name = sc.nextLine();
		
		PreparedStatement st = conn.prepareStatement("UPDATE employees SET name = ? WHERE id = ?");
		st.setString(1, name);
		st.setInt(2, id);
		int rows = st.executeUpdate();
		
		System.out.println(rows+" row(s) updated");
	}
	static public void deleteEmployee(Scanner sc, Connection conn) throws SQLException{
		System.out.println("Enter the id of the employee you want to delete: ");
		int id = sc.nextInt();
		sc.nextLine();
		
		PreparedStatement st = conn.prepareStatement("DELETE FROM employees WHERE id = ?");
		st.setInt(1, id);
		int rows = st.executeUpdate();
		
		System.out.println(rows+ " row(s) been deleted");
	}
}
