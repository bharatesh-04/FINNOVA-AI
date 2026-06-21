'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function InsightsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-primary-text">AI Insights</h1>

      <Card>
        <CardHeader>
          <CardTitle>Your Financial Insights</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-secondary-text">AI-powered insights about your spending patterns will appear here.</p>
        </CardContent>
      </Card>
    </div>
  );
}
