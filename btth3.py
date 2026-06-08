"""
    Người dùng nhập:
        seat_count
        ticket_class

            |
            v

    calculate_ticket_cost(seat_count, ticket_class)
        -> tính giá vé
        -> tính phí dịch vụ 5%
        -> return total_cost

            |
            v

    book_tickets(seat_count, total_cost)
        -> kiểm tra ghế trống
        -> available_seats -= seat_count
        -> flight_revenue += total_cost
        -> in xác nhận đặt vé

    Vì sao flight_revenue phải là biến toàn cục?
    Tổng doanh thu là dữ liệu dùng chung cho toàn bộ hệ thống.
    Chức năng đặt vé cần tăng doanh thu.
    Chức năng hoàn vé cần giảm doanh thu.
    Chức năng báo cáo cần đọc doanh thu hiện tại.

    Nếu để biến cục bộ (local variable), giá trị sẽ bị mất sau khi hàm kết thúc. 
    Vì vậy cần khai báo flight_revenue 
    là biến toàn cục để mọi hàm có thể truy cập và cập nhật cùng một nguồn dữ liệu.
"""

available_seats = 50
flight_revenue = 0.0
BASE_PRICE = 2000.0
MAX_CAPACITY = 50


def calculate_ticket_cost(ticket_count, ticket_class):
    """
    Tính tổng chi phí đặt vé.

    Args:
        ticket_count (int): Số lượng vé cần mua.
        ticket_class (int): Hạng vé.
            1 = Economy
            2 = Business

    Returns:
        float: Tổng chi phí sau khi cộng phí dịch vụ 5%.
    """
    if ticket_class == 1:
        ticket_price = BASE_PRICE
    else:
        ticket_price = BASE_PRICE * 1.5

    subtotal = ticket_price * ticket_count
    service_fee = subtotal * 0.05

    return subtotal + service_fee


def book_tickets(ticket_count, total_cost):
    """
    Xử lý đặt vé và cập nhật dữ liệu hệ thống.

    Args:
        ticket_count (int): Số lượng vé.
        total_cost (float): Tổng tiền thanh toán.

    Returns:
        bool: True nếu đặt vé thành công, False nếu thất bại.
    """
    global available_seats, flight_revenue

    if ticket_count > available_seats:
        print(f"Rất tiếc, chuyến bay chỉ còn {available_seats} chỗ trống.")
        return False

    available_seats -= ticket_count
    flight_revenue += total_cost

    print(f"Đặt vé thành công! Ghế trống còn lại: {available_seats}")
    return True


def cancel_tickets(ticket_count):
    """
    Hủy vé và hoàn tiền.

    Args:
        ticket_count (int): Số lượng vé cần hủy.

    Returns:
        float | None:
            Số tiền hoàn lại nếu thành công.
            None nếu hủy không hợp lệ.
    """
    global available_seats, flight_revenue

    if available_seats + ticket_count > MAX_CAPACITY:
        print("Lỗi: Số lượng vé hủy vượt quá số vé đã bán ra.")
        return None

    refund_amount = ticket_count * BASE_PRICE * 0.8

    available_seats += ticket_count
    flight_revenue -= refund_amount

    return refund_amount


def display_flight_status():
    """
    In báo cáo tình trạng chuyến bay.

    Báo cáo bao gồm:
    - Sức chứa tối đa
    - Số ghế đã đặt
    - Số ghế còn trống
    - Tổng doanh thu hiện tại

    Returns:
        None
    """
    booked_seats = MAX_CAPACITY - available_seats

    print("\n--- TÌNH TRẠNG CHUYẾN BAY VN2026 ---")
    print(f"Sức chứa tối đa: {MAX_CAPACITY}")
    print(f"Ghế đã đặt: {booked_seats}")
    print(f"Ghế trống: {available_seats}")
    print(f"Tổng doanh thu hiện tại: ${flight_revenue}")


def main():
    """
    Hàm điều khiển luồng chính của chương trình.

    Returns:
        None
    """
    while True:
        print("\n============= SKYBOOKING SYSTEM =============")
        print("Chuyến bay: VN2026 | Khởi hành: Hà Nội")
        print("1. Đặt vé máy bay")
        print("2. Hủy vé & Hoàn tiền")
        print("3. Xem tình trạng chuyến bay")
        print("4. Đóng hệ thống")
        print("=============================================")

        choice = input("Chọn chức năng (1-4): ")

        match choice:
            case "1":
                print("\n--- ĐẶT VÉ MÁY BAY ---")

                ticket_count = int(input("Nhập số lượng vé: "))

                if ticket_count <= 0:
                    print("Số lượng vé không hợp lệ.")
                    continue

                ticket_class = int(
                    input("Chọn hạng vé (1: Economy, 2: Business): ")
                )

                if ticket_class not in (1, 2):
                    print("Hạng vé không hợp lệ.")
                    continue

                total_cost = calculate_ticket_cost(
                    ticket_count,
                    ticket_class
                )

                if ticket_class == 1:
                    class_name = "Economy"
                    ticket_price = BASE_PRICE
                else:
                    class_name = "Business"
                    ticket_price = BASE_PRICE * 1.5

                subtotal = ticket_price * ticket_count
                service_fee = subtotal * 0.05

                print("-> Xác nhận đặt chỗ:")
                print(
                    f"Số lượng: {ticket_count} | Hạng: {class_name}"
                )
                print(f"Tạm tính: ${subtotal}")
                print(f"Phí dịch vụ (5%): ${service_fee}")
                print(f"Tổng thanh toán: ${total_cost}")

                book_tickets(ticket_count, total_cost)

            case "2":
                print("\n--- HỦY VÉ & HOÀN TIỀN ---")

                ticket_count = int(input("Nhập số lượng vé muốn hủy: "))

                if ticket_count <= 0:
                    print("Số lượng vé không hợp lệ.")
                    continue

                refund_amount = cancel_tickets(ticket_count)

                if refund_amount is not None:
                    print(
                        f"Hủy vé thành công. "
                        f"Hệ thống đã hoàn lại: "
                        f"${refund_amount} (80% giá cơ bản)."
                    )
                    print(
                        f"Ghế trống hiện tại: {available_seats}"
                    )

            case "3":
                display_flight_status()

            case "4":
                print("Đóng hệ thống thành công!")
                break

            case _:
                print("Lựa chọn không hợp lệ.")


main()