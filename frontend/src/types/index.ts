export interface Product {
  id: number;
  name: string;
  category: string;
  brand: string;
  price: number;
  stock_quantity: number;
  description: string;
  rating: number;
  tags: string;
  image_url: string;
  specs?: string;
  created_at: string;
  why_recommended?: string[];
  relevance_score?: number;
}

export interface ExtractedIntent {
  category?: string | null;
  max_budget?: number | null;
  min_budget?: number | null;
  brand?: string | null;
  use_case?: string | null;
  keywords: string[];
  features_requested: string[];
}

export interface AISearchResponse {
  query: string;
  extracted_intent: ExtractedIntent;
  response_message: string;
  products: Product[];
  out_of_stock_alert?: string | null;
  total_found: number;
}

export interface CartItem {
  id: number;
  session_id: string;
  product_id: number;
  quantity: number;
  product: Product;
  subtotal: number;
  is_stock_available: boolean;
  available_stock: number;
}

export interface CartSummary {
  items: CartItem[];
  subtotal: number;
  tax: number;
  shipping: number;
  total: number;
  item_count: number;
}

export interface OrderItem {
  id: number;
  product_id: number;
  product_name: string;
  unit_price: number;
  quantity: number;
  subtotal: number;
}

export interface Order {
  id: number;
  user_id?: number | null;
  customer_name: string;
  customer_email: string;
  customer_phone: string;
  shipping_address: string;
  payment_method: string;
  total_amount: number;
  status: string;
  created_at: string;
  items: OrderItem[];
}

export interface User {
  id: number;
  email: string;
  name: string;
  role: 'customer' | 'admin';
}

export interface AdminStats {
  total_products: number;
  total_orders: number;
  total_revenue: number;
  products_sold: number;
  low_stock_products: number;
}

export interface TopSellingProduct {
  product_id: number;
  product_name: string;
  category: string;
  units_sold: number;
  revenue_generated: number;
}

export interface DailySalesData {
  date: string;
  revenue: number;
  orders_count: number;
}

export interface AdminAnalytics {
  stats: AdminStats;
  sales_over_time: DailySalesData[];
  top_selling: TopSellingProduct[];
}

export interface CSVImportResult {
  success: boolean;
  imported_count: number;
  failed_count: number;
  errors: string[];
  sample_preview: any[];
}
