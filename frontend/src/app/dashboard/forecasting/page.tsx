'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function ForeccastingPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-primary-text">Expense Forecasting</h1>

      <Card>
        <CardHeader>
          <CardTitle>Future Expense Predictions</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-secondary-text">AI-powered expense forecasts based on your spending patterns.</p>
        </CardContent>
      </Card>
    </div>
  );
}
