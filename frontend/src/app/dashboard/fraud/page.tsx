'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function FraudPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-primary-text">Fraud Detection</h1>

      <Card>
        <CardHeader>
          <CardTitle>Suspicious Activity Alerts</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-secondary-text">AI-powered fraud detection to protect your finances.</p>
        </CardContent>
      </Card>
    </div>
  );
}
